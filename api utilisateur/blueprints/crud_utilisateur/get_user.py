from flask import jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from model_db import Utilisateur
from setting.auth  import payload_validator, authenticate_validator

get_user_bp = Blueprint("get_user", __name__)

@get_user_bp.route("/get_user", methods=["GET"])
@jwt_required()
def get_user():
    try:
        identity = get_jwt_identity()
        claims = get_jwt()
        authenticate_validator(identity= identity, claims= claims)

        if not Utilisateur.query.filter_by(identity['id_utilisateur']).role == "Admin":
            return jsonify({"error": "User not found"}), 401
        users = Utilisateur.query.all()
        return jsonify({"users": [user.to_dict() for user in users]}), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500