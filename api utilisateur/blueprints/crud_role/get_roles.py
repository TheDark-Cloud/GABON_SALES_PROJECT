from flask import Blueprint, jsonify, current_app
from setting.config import db
from setting.auth import authenticate_validator, payload_validator
from model_db import Role, Utilisateur
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

get_role_bp = Blueprint("get_role", __name__)

@get_role_bp.route("/roles", methods=["GET"])
@jwt_required()
def get_roles():
    try:
        identity = get_jwt_identity()
        claims = get_jwt()
        authenticate_validator(identity, claims)

        user = Utilisateur.query.get_or_404(identity["id_utilisateur"])
        if not user or user.is_complete == False:
            return jsonify({"error": "Authorisation denied due to user not found"}), 500

        if user.role.name_role != "admin":
            return jsonify({"error": "Authorisation privileges denied"}), 403
        if not user.role.name_role == "admin" and not user.rolename_role == claims['name_role']:
            return jsonify({"error": "Authorisation privileges denied"}), 403

        roles = Role.query.all()
        return jsonify({"roles":[role.to_dict() for role in roles]}), 200

    except Exception as ex:
        return jsonify({"error": f"Internal server error: {str(ex)}"}), 500