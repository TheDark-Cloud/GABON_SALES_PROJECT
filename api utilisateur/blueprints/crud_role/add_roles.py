from flask import jsonify, Blueprint, request
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from setting.config import db
from model_db import Role, Utilisateur
from setting.auth import authenticate_validator, payload_validator

add_role_bp = Blueprint("Add_role", __name__)

def check_role(role):
    try:
        #checks in the database
        if Role.query.filter_by(name_role=role).scalar() is not None:
            return jsonify({"message": "Role exists"}), 409
            #checks the format
        if not isinstance(role, str):
            return jsonify({f"message": f"Role {role} is not properly formated"}), 400
    except Exception as err:
        return jsonify({"error": str(err)}), 400


@add_role_bp.route("/add_role", methods=["POST"])
@jwt_required()
def add_role():
    try:
        claims = get_jwt()
        identity = get_jwt_identity()
        authenticate_validator(identity, claims)
        user = Utilisateur.query.get_or_404(identity["id_utilisateur"]).scalar().first()

        payload = request.get_json()
        payload_validator(payload)

        user = Utilisateur.query.get_or_404(identity["id_utilisateur"]).scalar()
        if not user:
            return jsonify({"message": "User required for authentification"}), 404
        if user.role.name_role == payload['name_role'] and user.role.name_role == claims['name_role'].lower():
            if isinstance(['name_role'], list):
                for each_role in payload['name_role']:
                    check_role(each_role)

                    db.session.add(Role(each_role.lower()))
                    db.session.commit()
                    db.session.close()
            if isinstance(payload['name_role'], str):
                check_role(payload['name_role'])
                db.session.add(Role(name_role=payload['name_role'].lower()))
                db.session.commit()
                db.session.close()
            return jsonify({"message": "Role added successfully"}), 201

        return jsonify({"error": "Authorisation privileges denied"}), 403
    except Exception as err:
        return jsonify({"error": str(err)}), 400