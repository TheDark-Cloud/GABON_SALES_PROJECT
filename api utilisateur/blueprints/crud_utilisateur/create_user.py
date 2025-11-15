from flask import Blueprint, request, jsonify
from setting.tokenize import tokenize
from model_db import Utilisateur, Role
from setting.config import db, hpw, is_valid_format

create_user_bp = Blueprint("create_user", __name__)

@create_user_bp.route("/create_user", methods=["POST"])
def create_user():
    """Create a new user
    expected JSON body: {mail: <email>, password: <password>, role: <role>}
    return: {user_data: <token>}
    """


    try:
        user_data = request.get_json(silent=True) or {}
        if user_data is None:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        required_fields = ["mail", "password", "role"]

        missing = [field for field in required_fields if field not in user_data]
        if missing:
            return jsonify({"error": f"Missing required fields: {missing}"}), 400

        if not isinstance(user_data.get("password"), str) or len(user_data.get("password"))<8:
            return jsonify({"error": "Password must be at least 8 chars"})
        if not is_valid_format(user_data.get("mail")):
            return jsonify({"error": "Invalid email format"})

        if Utilisateur.query.filter_by(mail=user_data.get("mail").strip().lower().scalar()):
            return jsonify({"error": "Email already in use"}), 409
        if Role.query.filter_by(role=user_data.get("role").strip().lower().scalar()):
            return jsonify({"error": "Role does not exist"}), 409

        user = Utilisateur(mail=user_data.get("mail").strip().lower(),
                           password=hpw(user_data.get("password")),
                           id_role=Role.query.filter_by(role=user_data.get("role")).first().role_id)
        db.session.add(user)
        db.session.commit()

        identity = {"id_utilisateur": user.utilisateur_id}
        claims = {"role": user.role}
        return jsonify({"user_data": tokenize(identity=identity, claims=claims)}), 201

    except Exception as ex:
        db.session.rollback()
        return jsonify({"error": {"message": str(ex)}}), 400

