import bcrypt
from flask import Blueprint, request, jsonify
import json
from model_db import Utilisateur
from extension import db
from flask_jwt_extended import create_access_token

utilisateur_bp = Blueprint('utilisateur', __name__)


# Creation des comptes
@utilisateur_bp.route('/utilisateur', methods=["POST"])
def create_user():
    """Creation de l'utilisateur avec selection du role"""

    data = request.get_json() or {}

    email = data.get('email')
    password = data.get('password')
    id_role = data.get('id_role')

    if not email or not password or not id_role:
        return jsonify({"error":"email, password, role requis."}), 400

    # checking if the email is already in the database
    if Utilisateur.query.filter_by(email=email).first():
        return jsonify({'error':"L'addresse email existe deja"}), 409

    hashed_password = hashPasword(password)
    # sending the data in the database
    try:
        user = Utilisateur(email=email,
                           password= hashed_password,
                           id_role=id_role)

        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500

    payload = {
        "id_utilisateur": user.id_utilisateur,
        "id_role": user.id_role,
        "email": user.email
    }
    # JWT tokenization
    # jwt_token = create_access_token(identity=user.id_utilisateur,
    #                                 additional_claims={"id_role": id_role, 'email': email, "scope": "onboarding"},
    #                                 expires_delta=extension.ONBOARDING_EXPIRES)
    jwt_token = create_access_token(identity=json.dumps(payload))
    reponse = {
        "access_token": jwt_token,
    }
    return jsonify(reponse), 201

# Lire un utilisateur
@utilisateur_bp.route('/utilisateur/<int:id>', methods=["GET"])
def get_user(id):
    user = Utilisateur.query.get_or_404(id)
    if not user:
        return jsonify({'message':'Aucun comtpe n\'est associee a ce mail.'}), 404
    return jsonify({'user': user.id_utilisateur,
                    'email':user.email,
                    'password':user.password,
                    'id_role':user.id_role}), 200

# Mettre a jour un utilisateur
@utilisateur_bp.route('/utilisateur/mise-a-jour/<int:id>', methods=["PUT"])
def update_user(id):
    user = Utilisateur.query.get_or_404(id)
    data = request.get_json() or {}


    if 'email' in data:
        user.email = data['email']
        db.session.commit()

    elif 'password' in data:
        user.password = hashPasword(data['password'])
        db.session.commit()

    else:
        db.session.rollback()
        return jsonify({'message':'Veuille saisir vos informations.'}), 404
    return jsonify({'message': 'Compte mis à jour'}), 200

@utilisateur_bp.route('/utilisateur/delete/<int:id>', methods=["DELETE"])
def delete_user(id):
    user = Utilisateur.query.get_or_404(id)
    if not user:
        db.session.rollback()
        return jsonify({'Error': 'Compte introuvable'}), 404
    else:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Compte efface avec succes.'}), 200


# hashing the password
def hashPasword(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')