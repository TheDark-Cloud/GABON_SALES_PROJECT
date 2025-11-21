from flask import Blueprint, request, jsonify
from setting.tokenize import tokenize
from model_db import Utilisateur, Role
from setting.config import db, hpw, is_valid_format

create_user_bp = Blueprint("create_user", __name__)

@create_user_bp.route("/create_user", methods=["POST"])
def create_user():
    """Create a new user
    expected JSON body: {mail: <email>, password: <password>, name_role: <role>}
    return: {user_data: <token>}
    """


    try:
        user_data = request.get_json(silent=True) or {}
        if user_data is None:
            return jsonify({"error": "Invalid or missing JSON body"}), 400

        required_fields = ["mail", "password", "name_role"]

        missing = [field for field in required_fields if field not in user_data]
        if missing:
            return jsonify({"error": f"Missing required fields: {missing}"}), 400

        if not isinstance(user_data.get("password"), str) or len(user_data.get("password"))<=8:
            return jsonify({"error": "Password must be at least 8 chars"})
        if not is_valid_format(user_data.get("mail")):
            return jsonify({"error": "Invalid email format"}), 400

        if Utilisateur.query.filter_by(mail=user_data.get("mail").strip().lower()).scalar() is not None:
            return jsonify({"error": "Email already in use"}), 409
        if Role.query.filter_by(name_role=user_data.get("name_role").strip().lower()).scalar() is None:
            return jsonify({"error": "Role does not exist"}), 203

        user = Utilisateur(mail=user_data.get("mail").strip().lower(),
                           hashed_password=hpw(user_data.get("password")),
                           id_role=Role.query.get(name_role=user_data.get("name_role")).first().role_id,
                           is_complete=False)

        db.session.add(user)
        db.session.commit()
        db.session.close()
        identity = {"id_utilisateur": user.utilisateur_id}
        claims = {"name_role": user.role, "is_complete": user.is_complete}
        return jsonify({"user_data": tokenize(identity=identity, claims=claims)}), 201

    except Exception as ex:
        db.session.rollback()
        db.session.close()
        return jsonify({"error": {"message": str(ex)}}), 400

