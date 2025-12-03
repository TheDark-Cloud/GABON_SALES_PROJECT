from flask import jsonify, request, Blueprint
from flask_jwt_extended import get_jwt_identity, get_jwt, jwt_required
from model_db import Utilisateur
from setting.config import db
from setting.auth import authenticate_validator

delete_user_bp = Blueprint("delete_user", __name__)

@delete_user_bp.route("/delete_user", methods=["DELETE"])
@jwt_required
def delete_user():

    try:
        identity = get_jwt_identity()
        claims = get_jwt()
        authenticate_validator(identity, claims)

        user = Utilisateur.query.get_or_404(id_utilisateur=identity["id_utilisateur"]).delete()
        if not user:
            return jsonify({"error": "User not found."}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully."}), 200
    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": str(ex)}), 500