from flask import jsonify, Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from model_db import Utilisateur

get_user_bp = Blueprint("get_user", __name__)

@get_user_bp.route("/get_user", methods=["GET"])
@jwt_required()
def get_user():
    try:
        identity = get_jwt_identity()
        claims = get_jwt()

        if not identity or not isinstance(identity, dict):
            return jsonify({"error": "Invalid credentials"}), 401

        if claims is not None and isinstance(claims, dict):
            if Utilisateur.query.filter_by(identity['id_utilisateur']).role == "Admin":
                users = Utilisateur.query.all()
                return jsonify({"users": [user.to_dict() for user in users]}), 200

        return jsonify({"user_data": Utilisateur.query.get_or_404(identity["id_utilisateur"])}), 200
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500