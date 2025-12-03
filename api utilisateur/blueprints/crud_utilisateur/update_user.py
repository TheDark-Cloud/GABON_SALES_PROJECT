from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import jsonify, Blueprint, request
from model_db import Utilisateur
from setting.auth import authenticate_validator, payload_validator
from setting.config import db, validate_parameters, hpw

update_user_bp = Blueprint("update_user", __name__)

@update_user_bp.route("/update_user", methods=["PUT"])
@jwt_required()
def update_user():
    """ Updating the user"""

    try:
        identity = get_jwt_identity()
        claims = get_jwt()
        authenticate_validator(identity=identity, claims=claims)

        new_data = request.get_json()
        required_fields = ["mail", "password", "phone_number", "name_role"]
        payload_validator(payload=new_data, required_fields=required_fields)

        user = Utilisateur.query.filter_by(identity['id_utilisateur']).role== claims['name_role']
        if not user:
            return jsonify({"message": "User not found"}), 404

        if not validate_parameters(new_data.get("mail"), new_data.get("password"), new_data.get("phone_number")):
            return jsonify({"error": "Invalide fields"}), 400

        user.mail = new_data.get("mail")
        user.password = new_data.get("password")
        user.phone_number = new_data.get("phone_number")
        db.session.commit()
        return jsonify({"message": "User updated successfully"}), 200

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500