from flask import Blueprint, request, jsonify

from setting.auth import payload_validator
from setting.tokenize import tokenize
from model_db import Utilisateur, Role
from setting.config import db, hpw, is_valid_email_format

create_user_bp = Blueprint("create_user", __name__)

@create_user_bp.route("/create_user", methods=["POST"])
def create_user():
    """
    Creating a user

    The expected JSON body:
    identity {mail: <mail>, password: <password>}
    claims {name_role: <role>
    return: {user_data: <token>}
    """

    try:
        user_data = request.get_json(silent=True) or {} # getting user data
        required_fields = ["mail", "password", "phone_number", "name_role"] # what should be in the user data
        payload_validator(payload=user_data, required_fields=required_fields) # validating fields

        # password check
        if not isinstance(user_data.get("password"), str) or len(user_data.get("password"))<=8:
            return jsonify({"error": "Password must be at least 8 chars"})
        # Mail check
        if not is_valid_email_format(user_data.get("mail")):
            return jsonify({"error": "Invalid email format"}), 400
        # Phone check
        if not (isinstance(user_data.get('phone_number'), str) and len(user_data.get('phone_number')) == 9):
            return jsonify({"error": "Invalid phone number format"}), 400

        if Utilisateur.query.filter_by(mail=user_data.get("mail")).scalar() is not None:
            return jsonify({"error": "Email already in use"}), 409

        role = Role.query.filter_by(name_role=user_data.get("name_role")).scalar()
        if role is None:
            return jsonify({"error": "Role does not exist"}), 203


        try:
            user = Utilisateur(mail=user_data.get("mail"),
                               hashed_password=hpw(user_data.get("password")),
                               phone_number=user_data.get("phone_number"),
                               id_role=role.id_role,
                               is_complete=False)
            db.session.add(user)
            db.session.commit()

            identity = str(user.id_utilisateur)
            claims = {"name_role": role.name_role, "is_complete": user.is_complete}
        except Exception as ex:
            db.session.rollback()
            return jsonify({"error": {"message": str(ex)}}), 400
        # Loading the token
        creation_token = tokenize(identity=identity, claims=claims)
        db.session.close()
        return jsonify({"token": creation_token}), 201
    except Exception as ex:
        db.session.rollback()
        db.session.close()
        return jsonify({"error": {"message": str(ex)}}), 400

