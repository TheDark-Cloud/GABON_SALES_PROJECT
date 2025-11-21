from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from functools import wraps
from extension import db, generate_token, decode_token
from model_db import Utilisateur

utilisateur_bp = Blueprint("utilisateur", __name__)

def _normalize_email(email):
    return (email or "").strip().lower()

def _json_or_bad_request():
    data = request.get_json(silent=True)
    if data is None:
        return None, jsonify({"error": {"message": "Invalid or missing JSON body"}}), 400
    return data, None, None

def _extract_bearer_token():
    auth = request.headers.get("Authorization", "")
    if not auth:
        return None, (jsonify({"error": {"message": "Missing Authorization header"}}), 401)
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None, (jsonify({"error": {"message": "Invalid Authorization header format"}}), 401)
    return parts[1], None

def require_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token, err = _extract_bearer_token()
        if err:
            return err
        try:
            payload = decode_token(token)
        except ValueError as e:
            current_app.logger.info("Token decode error: %s", e)
            return jsonify({"error": {"message": str(e)}}), 401
        if not isinstance(payload, dict):
            return jsonify({"error": {"message": "Invalid token payload"}}), 401
        # attach payload to request context via kwargs for handler use
        kwargs["_token_payload"] = payload
        return fn(*args, **kwargs)
    return wrapper

def _authorize_action_on_user(token_payload: dict, target_user_id: int):
    """
    Returns (True, None) if allowed, otherwise (False, (response, status))
    Policy:
      - Allow if token_payload['id_utilisateur'] == target_user_id
      - Allow if token_payload['id_role'] == 1 (admin)
      - Otherwise deny 403
    """
    try:
        token_user = int(token_payload.get("id_utilisateur"))
    except Exception:
        return False, (jsonify({"error": {"message": "Invalid token identity"}}), 401)
    token_role = token_payload.get("id_role")
    if token_user == int(target_user_id) or token_role == 1:
        return True, None
    return False, (jsonify({"error": {"message": "Forbidden"}}), 403)

@utilisateur_bp.route("/user", methods=["POST"]) # OK
def create_user():
    """Create new user (public)"""
    data, err_resp, status = _json_or_bad_request()
    if err_resp:
        return err_resp, status

    email = _normalize_email(data.get("email"))
    password = data.get("password")
    id_role = data.get("id_role")

    if not email or not password or id_role is None:
        return jsonify({"error": {"message": "email, password, id_role required"}}), 400
    if not isinstance(password, str) or len(password) < 8:
        return jsonify({"error": {"message": "Password must be >= 8 chars"}}), 400

    try:
        # Pass raw password to model if your model hashes it; otherwise store hashed
        # Here we pass hashed password to be consistent with model_db expecting password_hash
        user = Utilisateur(mail=email, password=generate_password_hash(password), id_role=id_role)
        db.session.add(user)
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
        current_app.logger.warning("IntegrityError creating user: %s", ie)
        return jsonify({"error": {"message": "Email already exists or constraint violation"}}), 409
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("DB error creating user")
        return jsonify({"error": {"message": "Internal server error"}}), 500

    identity = {"id_utilisateur": user.id_utilisateur, "id_role": user.id_role}
    try:
        token = generate_token(identity)
    except Exception:
        current_app.logger.exception("Token generation failed")
        token = None

    return jsonify({"data": {"access_token": token, "user": user.to_dict()}}), 201

@utilisateur_bp.route("/user/<int:user_id>", methods=["GET"]) # OK
@require_token
def get_user(user_id, _token_payload=None):
    """Get a user by ID from the database (requires token)"""
    allowed, err = _authorize_action_on_user(_token_payload, user_id)
    if not allowed:
        return err

    user = Utilisateur.query.get_or_404(user_id)
    return jsonify({"data": user.to_dict()}), 200

@utilisateur_bp.route("/user/<int:user_id>", methods=["PUT"]) # OK
@require_token
def update_user(user_id, _token_payload=None):
    """Update user fields email and/or password (requires token)"""
    allowed, err = _authorize_action_on_user(_token_payload, user_id)
    if not allowed:
        return err

    user = Utilisateur.query.get_or_404(user_id)
    data, err_resp, status = _json_or_bad_request()
    if err_resp:
        return err_resp, status

    updated = False

    if "email" in data:
        new_email = _normalize_email(data["email"])
        if not new_email:
            return jsonify({"error": {"message": "email cannot be empty"}}), 400
        exists = Utilisateur.query.filter(Utilisateur.email == new_email, Utilisateur.id_utilisateur != user_id).first()
        if exists:
            return jsonify({"error": {"message": "Email already in use"}}), 409
        user.email = new_email
        updated = True

    if "password" in data:
        pwd = data["password"]
        if not isinstance(pwd, str) or len(pwd) < 8:
            return jsonify({"error": {"message": "Password must be at least 8 chars"}}), 400
        user.hashed_password = generate_password_hash(pwd)
        updated = True

    if not updated:
        return jsonify({"error": {"message": "No updatable fields provided"}}), 400

    try:
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
        current_app.logger.warning("IntegrityError updating user %s: %s", user_id, ie)
        return jsonify({"error": {"message": "Conflict updating user"}}), 409
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("DB error updating user %s", user_id)
        return jsonify({"error": {"message": "Internal server error"}}), 500

    return jsonify({"data": user.to_dict()}), 200

@utilisateur_bp.route("/user/<int:user_id>", methods=["DELETE"]) # OK
@require_token
def delete_user(user_id, _token_payload=None):
    """Delete a user (requires token)"""
    allowed, err = _authorize_action_on_user(_token_payload, user_id)
    if not allowed:
        return err

    user = Utilisateur.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("DB error deleting user %s", user_id)
        return jsonify({"error": {"message": "Internal server error"}}), 500
    return "", 204

