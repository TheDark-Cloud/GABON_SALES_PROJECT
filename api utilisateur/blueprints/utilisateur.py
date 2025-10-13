from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from extension import db, generate_token, decode_token
from model_db import Utilisateur

utilisateur_bp = Blueprint("utilisateur", __name__)

def _normalize_email(email):
    return (email or "").strip().lower()

@utilisateur_bp.route("/user", methods=["POST"])
def create_user():
    """Create new user"""

    # getting the date from the front
    data = request.get_json(silent=True) or {}
    email = _normalize_email(data.get("email"))
    password = data.get("password")
    id_role = data.get("id_role")

    # checking that all the date are not empty
    if not email or not password or id_role is None:
        return jsonify({"error": {"message": "email, password, id_role required"}}), 400
    # checking that the password meets standards
    if len(password) < 8:
        return jsonify({"error": {"message": "Password must be >= 8 chars"}}), 400
    # checking for duplicate value
    if Utilisateur.query.filter_by(email=email).first():
        return jsonify({"error": {"message": "Email already exists"}}), 409

    # inserting into the database
    try:
        user = Utilisateur(email=email, password=password, id_role=id_role)
        db.session.add(user)
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
        current_app.logger.warning("IntegrityError creating user: %s", ie)
        return jsonify({"error": {"message": "Conflict creating user"}}), 409
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("DB error creating user")
        return jsonify({"error": {"message": "Internal server error"}}), 500
    identity = {"id_utilisateur": user.id_utilisateur, "id_role": user.id_role}
    # token = create_access_token(identity=identity)

    token = generate_token(identity)

    return jsonify({"data": {"access_token": token, "user": user.to_dict()}}), 201

@utilisateur_bp.route("/user/get_user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """Getting user from database"""
    user = Utilisateur.query.get_or_404(user_id)
    if not user:
        return jsonify({"error": {"message": "User not found"}}), 404
    return jsonify({"data": user.to_dict()}), 200

@utilisateur_bp.route("/user/update_user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """Updating user in the databased"""
    user = Utilisateur.query.get_or_404(user_id)
    data = request.get_json(silent=True) or {}
    updated = False

    # checking that we are receiving information to update
    if "email" in data:
        new_email = _normalize_email(data["email"])
        if Utilisateur.query.filter(Utilisateur.email == new_email, Utilisateur.id_utilisateur != user_id).first():
            return jsonify({"error": {"message": "Email already in use"}}), 409
        user.email = new_email
        updated = True
    if "password" in data:
        pwd = data["password"]
        if not pwd or len(pwd) < 8:
            return jsonify({"error": {"message": "Password must be at least 8 chars"}}), 400
        user.password_hash = generate_password_hash(pwd)
        updated = True

    # returning an error if nothing has been entered
    if not updated:
        return jsonify({"error": {"message": "No updatable fields provided"}}), 400
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception(f"DB error updating user {user_id}")
        return jsonify({"error": {"message": "Internal server error"}}), 500
    return jsonify({"data": user.to_dict()}), 200


@utilisateur_bp.route("/user/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = Utilisateur.query.get_or_404(user_id)
    try:
        db.session.delete(user)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("DB error deleting user %s", user_id)
        return jsonify({"error": {"message": "Internal server error"}}), 500
    return "", 204










# import bcrypt
# from flask import Blueprint, request, jsonify
# import json
# from model_db import Utilisateur
# from extension import db
# from flask_jwt_extended import create_access_token
# from datetime import timedelta
#
# utilisateur_bp = Blueprint('utilisateur', __name__)
#
#
# # Creation des comptes
# @utilisateur_bp.route('/utilisateur', methods=["POST"])
# def create_user():
#     """Creation de l'utilisateur avec selection du role"""
#
#     data = request.get_json() or {}
#
#     email = data.get('email')
#     password = data.get('password')
#     id_role = data.get('id_role')
#
#     if not email or not password or not id_role:
#         return jsonify({"error":"email, password, role requis."}), 400
#
#     # checking if the email is already in the database
#     if Utilisateur.query.filter_by(email=email).first():
#         return jsonify({'error':"L'addresse email existe deja"}), 409
#
#     hashed_password = hashPasword(password)
#     # sending the data in the database
#     try:
#         user = Utilisateur(email=email,
#                            password= hashed_password,
#                            id_role=id_role)
#
#         db.session.add(user)
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"error":str(e)}), 500
#
#     payload = {
#         "id_utilisateur": user.id_utilisateur,
#         "id_role": user.id_role,
#     }
#
#     jwt_token = create_access_token(identity=json.dumps(payload))
#     reponse = {
#         "access_token": jwt_token,
#     }
#     return jsonify(reponse), 201
#
# # Lire un utilisateur
# @utilisateur_bp.route('/utilisateur/<int:id>', methods=["GET"])
# def get_user(id):
#     user = Utilisateur.query.get_or_404(id)
#     if not user:
#         return jsonify({'message':'Aucun comtpe n\'est associee a ce mail.'}), 404
#     return jsonify({'user': user.id_utilisateur,
#                     'email':user.email,
#                     'password':user.password,
#                     'id_role':user.id_role}), 200
#
# # Mettre a jour un utilisateur
# @utilisateur_bp.route('/utilisateur/mise-a-jour/<int:id>', methods=["PUT"])
# def update_user(id):
#     user = Utilisateur.query.get_or_404(id)
#     data = request.get_json() or {}
#
#
#     if 'email' in data:
#         user.email = data['email']
#         db.session.commit()
#
#     elif 'password' in data:
#         user.password = hashPasword(data['password'])
#         db.session.commit()
#
#     else:
#         db.session.rollback()
#         return jsonify({'message':'Veuille saisir vos informations.'}), 404
#     return jsonify({'message': 'Compte mis à jour'}), 200
#
# @utilisateur_bp.route('/utilisateur/delete/<int:id>', methods=["DELETE"])
# def delete_user(id):
#     user = Utilisateur.query.get_or_404(id)
#     if not user:
#         db.session.rollback()
#         return jsonify({'Error': 'Compte introuvable'}), 404
#     else:
#         db.session.delete(user)
#         db.session.commit()
#         return jsonify({'message': 'Compte efface avec succes.'}), 200
#
#
# # hashing the password
# def hashPasword(password):
#     return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')