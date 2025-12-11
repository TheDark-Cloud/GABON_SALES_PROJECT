from flask import Blueprint, request, jsonify
from setting.tokenize import tokenize
from setting.config import is_valid_email_format, is_valid_password_format
from werkzeug.security import check_password_hash
from model_db import db, Utilisateur, Vendeur, Client
from setting.auth import payload_validator

log_in_bp = Blueprint("auth", __name__)

@log_in_bp.route("/user/login", methods=['POST'])
def login():
    data = request.get_json(silent=True) or {}
    required_fields = ['mail', 'password']
    payload_validator(payload=data, required_fields=required_fields)

    try:
        if not is_valid_email_format(data.get('mail')):
            return jsonify({"error": "Invalid email format"}), 400
        if not is_valid_password_format(data.get('password')):
            return jsonify({"error": "Invalid password format"}), 400

        # Fetch user
        user = Utilisateur.query.filter_by(mail=data.get('mail')).first()
        if not user or not check_password_hash(user.hashed_password, data.get('password')):
            return jsonify({"error": "Invalid credentials"}), 401

        # Base claims
        claims = {
            "name_role": user.role.name_role,
            "is_complete": user.is_complete
        }

        # Detect vendeur or client
        vendeur = Vendeur.query.filter_by(id_utilisateur=user.id_utilisateur).first()
        client = Client.query.filter_by(id_utilisateur=user.id_utilisateur).first()

        if vendeur:
            claims["name_role"] = "vendeur"
            claims["id_vendeur"] = vendeur.id_vendeur

        elif client:
            claims["name_role"] = "client"
            claims["id_client"] = client.id_client

        # Generate token
        login_token = tokenize(identity=user.id_utilisateur, claims=claims)

        return jsonify({"login_token": login_token}), 200

    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": {"message": str(ex)}}), 400