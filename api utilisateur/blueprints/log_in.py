from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.exc import SQLAlchemyError
from model_db import Utilisateur
from extension import db

log_in_bp = Blueprint("auth", __name__, url_prefix="/auth")

def _build_identity(user):
    return {"id_utilisateur": user.id_utilisateur, "id_role": user.id_role,
            "is_admin": getattr(user.role, "nom_role", "").lower() in ("admin", "administrateur")}

@log_in_bp.route("/login", methods=["POST"])
def account_login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": {"message": "Email and password required"}}), 400
    try:
        user = Utilisateur.query.filter_by(email=email).first()
    except SQLAlchemyError:
        current_app.logger.exception("DB error during login")
        return jsonify({"error": {"message": "Internal server error"}}), 500

    if not user or not user.verify_password(password):
        current_app.logger.info("Failed login attempt for email %s", email)
        return jsonify({"error": {"message": "Invalid credentials"}}), 401

    identity = _build_identity(user)
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)

    return jsonify({"data": {"access_token": access_token, "refresh_token": refresh_token, "user": user.to_dict()}}), 200