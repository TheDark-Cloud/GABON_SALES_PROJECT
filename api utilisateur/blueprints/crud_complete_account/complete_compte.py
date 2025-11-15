# from flask import Blueprint, request, jsonify, current_app
# from functools import wraps
# from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# from extension import db, decode_token
# from model_db import Vendeur, Client, Utilisateur
#
# complete_compte_bp = Blueprint("complete_compte", __name__)
#
# def _validate_payload(payload, required):
#     missing = [p for p in required if not payload.get(p)]
#     if missing:
#         return False, f"Missing required fields: {', '.join(missing)}"
#     return True, None
#
# def _extract_bearer_token():
#     auth = request.headers.get("Authorization", "")
#     if not auth:
#         return None, (jsonify({"error": {"message": "Missing Authorization header"}}), 401)
#     parts = auth.split()
#     if len(parts) != 2 or parts[0].lower() != "bearer":
#         return None, (jsonify({"error": {"message": "Invalid Authorization header format"}}), 401)
#     return parts[1], None
#
# def require_token(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         token, err = _extract_bearer_token()
#         if err:
#             return err
#         try:
#             payload = decode_token(token)
#         except ValueError as e:
#             current_app.logger.info("Token decode error: %s", e)
#             return jsonify({"error": {"message": str(e)}}), 401
#         if not isinstance(payload, dict):
#             return jsonify({"error": {"message": "Invalid token payload"}}), 401
#         kwargs["_token_payload"] = payload
#         return fn(*args, **kwargs)
#     return wrapper
#
# @complete_compte_bp.route("/user/account/vendeur_client/complete", methods=["POST"])
# @require_token
# def create_compte(_token_payload=None):
#     """
#     Complete a Vendeur or Client account.
#     Token payload must include id_utilisateur and id_role.
#     Token must be sent in Authorization header as Bearer <token>.
#     """
#     payload = _token_payload
#     id_utilisateur = payload.get("id_utilisateur")
#     id_role = payload.get("id_role")
#     if id_utilisateur is None or id_role is None:
#         return jsonify({"error": {"message": "Token missing identity fields"}}), 400
#
#     user = Utilisateur.query.get(id_utilisateur)
#     if not user:
#         return jsonify({"error": {"message": "Utilisateur introuvable"}}), 404
#
#     if user.id_role != id_role:
#         return jsonify({"error": {"message": "Role mismatch"}}), 403
#
#     data = request.get_json(silent=True) or {}
#
#     if id_role == 2:
#         if user.vendeur is not None:
#             return jsonify({"error": {"message": "Compte vendeur déjà complété"}}), 409
#         ok, err = _validate_payload(data, ["nom", "prenom", "numero", "identite"])
#         if not ok:
#             return jsonify({"error": {"message": err}}), 400
#         try:
#             new_vendeur = Vendeur(
#                 nom=data["nom"].strip(),
#                 prenom=data["prenom"].strip(),
#                 numero=data["numero"].strip(),
#                 identite=data["identite"].strip(),
#                 id_utilisateur=id_utilisateur
#             )
#             db.session.add(new_vendeur)
#         except ValueError as ve:
#             return jsonify({"error": {"message": str(ve)}}), 400
#
#     elif id_role == 3:
#         if user.client is not None:
#             return jsonify({"error": {"message": "Compte client déjà complété"}}), 409
#         ok, err = _validate_payload(data, ["nom", "prenom", "numero"])
#         if not ok:
#             return jsonify({"error": {"message": err}}), 400
#         try:
#             new_client = Client(
#                 nom=data["nom"].strip(),
#                 prenom=data["prenom"].strip(),
#                 numero=data["numero"].strip(),
#                 id_utilisateur=id_utilisateur
#             )
#             db.session.add(new_client)
#         except ValueError as ve:
#             return jsonify({"error": {"message": str(ve)}}), 400
#
#     else:
#         return jsonify({"error": {"message": "Role non autorisé"}}), 403
#
#     try:
#         db.session.commit()
#     except IntegrityError as ie:
#         db.session.rollback()
#         current_app.logger.warning("IntegrityError in complete_compte: %s", ie)
#         return jsonify({"error": {"message": "Conflit de données (valeurs uniques)"}}), 409
#     except SQLAlchemyError:
#         db.session.rollback()
#         current_app.logger.exception("DB error in complete_compte")
#         return jsonify({"error": {"message": "Internal server error"}}), 500
#
#     return jsonify({"data": {"message": "Votre compte a été complété avec succès"}}), 201

from flask import Blueprint, request, jsonify, current_app
from functools import wraps
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from extension import db, decode_token
from model_db import Vendeur, Client, Utilisateur

# Blueprint grouping for account completion endpoints
complete_compte_bp = Blueprint("complete_compte", __name__)

# Helper: validate required fields exist and are non-empty in payload
def _validate_payload(payload, required):
    missing = [p for p in required if not payload.get(p)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None

# Helper: extract bearer token from Authorization header
# Returns (token, None) on success or (None, (response, status)) on failure
def _extract_bearer_token():
    auth = request.headers.get("Authorization", "")
    if not auth:
        return None, (jsonify({"error": {"message": "Missing Authorization header"}}), 401)
    parts = auth.split()
    # Expect exactly "Bearer <token>"
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None, (jsonify({"error": {"message": "Invalid Authorization header format"}}), 401)
    return parts[1], None

# Decorator: requires a valid decoded token; attaches payload as _token_payload kwarg
def require_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # 1) Extract token string
        token, err = _extract_bearer_token()
        if err:
            return err  # err is already (response, status)

        # 2) Decode token and handle expected failures
        try:
            payload = decode_token(token)
        except ValueError as e:
            # decode_token raises ValueError for known token problems (expired, invalid, etc.)
            current_app.logger.info("Token decode error: %s", e)
            return jsonify({"error": {"message": str(e)}}), 401
        except Exception:
            # Unexpected errors while decoding
            current_app.logger.exception("Unexpected token decode failure")
            return jsonify({"error": {"message": "Invalid token"}}), 401

        # 3) Ensure payload format is what we expect
        if not isinstance(payload, dict):
            return jsonify({"error": {"message": "Invalid token payload"}}), 401

        # 4) Attach payload for the view function and continue
        kwargs["_token_payload"] = payload
        return fn(*args, **kwargs)
    return wrapper

@complete_compte_bp.route("/user/account/vendeur_client/complete", methods=["POST"])
@require_token
def create_compte(_token_payload=None):
    """
    Complete a Vendeur or Client account.
    - Token payload must include id_utilisateur and id_role.
    - Token must be sent in Authorization header as Bearer <token>.
    - Role mapping expected: 2 => Vendeur, 3 => Client.
    """
    # --- Validate token identity fields ---
    payload = _token_payload or {}
    id_utilisateur = payload.get("id_utilisateur")
    id_role = payload.get("id_role")
    if id_utilisateur is None or id_role is None:
        return jsonify({"error": {"message": "Token missing identity fields"}}), 400

    # --- Load the base Utilisateur record and confirm role consistency ---
    user = Utilisateur.query.get(id_utilisateur)
    if not user:
        return jsonify({"error": {"message": "Utilisateur introuvable"}}), 404
    if user.id_role != id_role:
        # Prevent a token for one role from completing an account for another role
        return jsonify({"error": {"message": "Role mismatch"}}), 403

    # --- Parse JSON body safely; use empty dict if missing to yield useful validation errors ---
    data = request.get_json(silent=True) or {}

    # --- Vendeur completion flow (role == 2) ---
    if int(id_role) == 2:
        # Prevent duplicate completion if a related Vendeur already exists
        if getattr(user, "vendeur", None) is not None:
            return jsonify({"error": {"message": "Compte vendeur déjà complété"}}), 409

        # Validate required fields for vendor; identite required for vendeur
        ok, err = _validate_payload(data, ["nom", "prenom", "numero", "identite"])
        if not ok:
            return jsonify({"error": {"message": err}}), 400

        # Create Vendeur instance and add to session
        try:
            new_vendeur = Vendeur(
                nom=data["nom"].strip(),
                prenom=data["prenom"].strip(),
                numero=data["numero"].strip(),
                identite=data["identite"].strip(),
                id_utilisateur=id_utilisateur
            )
            db.session.add(new_vendeur)
        except ValueError as ve:
            # Model-level validation raising ValueError (if any)
            return jsonify({"error": {"message": str(ve)}}), 400

    # --- Client completion flow (role == 3) ---
    elif int(id_role) == 3:
        # Prevent duplicate completion if a related Client already exists
        if getattr(user, "client", None) is not None:
            return jsonify({"error": {"message": "Compte client déjà complété"}}), 409

        # Validate required fields for client (no identite required)
        ok, err = _validate_payload(data, ["nom", "prenom", "numero"])
        if not ok:
            return jsonify({"error": {"message": err}}), 400

        # Create Client instance and add to session
        try:
            new_client = Client(
                nom=data["nom"].strip(),
                prenom=data["prenom"].strip(),
                numero=data["numero"].strip(),
                id_utilisateur=id_utilisateur
            )
            db.session.add(new_client)
        except ValueError as ve:
            # Model-level validation raising ValueError (if any)
            return jsonify({"error": {"message": str(ve)}}), 400

    # --- Unsupported roles ---
    else:
        return jsonify({"error": {"message": "Role non autorisé"}}), 403

    # --- Commit transaction with robust error handling ---
    try:
        db.session.commit()
    except IntegrityError as ie:
        # Unique constraint or other integrity problems; rollback and return conflict
        db.session.rollback()
        current_app.logger.warning("IntegrityError in complete_compte: %s", ie)
        return jsonify({"error": {"message": "Conflit de données (valeurs uniques)"}}), 409
    except SQLAlchemyError:
        # Generic DB error; rollback and return 500
        db.session.rollback()
        current_app.logger.exception("DB error in complete_compte")
        return jsonify({"error": {"message": "Internal server error"}}), 500

    # --- Success response ---
    return jsonify({"data": {"message": "Votre compte a été complété avec succès"}}), 201