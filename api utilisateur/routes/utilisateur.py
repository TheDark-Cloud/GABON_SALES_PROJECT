from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import extension
from model_db import Utilisateur
from extension import db
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)


utilisateur_bp = Blueprint('utilisateur', __name__)


# Creation des comptes
@utilisateur_bp.route('/utilisateur', methods=["POST"])
def create_user():
    """Creation de l'utilisateur avec selection du role"""

    data = request.get_json() or {}

    email = data.get('email')
    hsh_password = generate_password_hash(data.get('password'))
    id_role = data.get('role_id')

    if not all([email, hsh_password, id_role]):
        return jsonify({"error":"email, mot_de_passe, role requis."}), 400

    # checking if the email is already in the database
    if Utilisateur.query.filter_by(email=email).first():
        return jsonify({'error':"L'addresse email existe deja"}), 409

    # sending the data in the database
    try:
        user = Utilisateur(email=email,
                           password= hsh_password,
                           id_role=id_role)

        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":str(e)}), 500

    # JWT tokenization
    jwt_token = create_access_token(identity=user.id_utilisateur,
                                           additional_claims={"id_role": id_role, 'email': email, "scope": "onboarding"},
                                            expires_delta=extension.ONBOARDING_EXPIRES)

    return jsonify({'message':'Compte cree avec succes','token': jwt_token}), 201

# Lire un utilisateur
@utilisateur_bp.route('/utilisateur/<string:email>', methods=["GET"])
def get_user(email):
    user = Utilisateur.query.get_or_404(email)
    if not user:
        return jsonify({'message':'Le utilisateur non existant.'}), 404
    return jsonify({'user': user.id,
                    'email':user.emai,
                    'nom_role':user.nom_role}), 200

# Mettre a jour un utilisateur
@utilisateur_bp.route('/utilisateur/<int:id>', methods=["PUT"])
def update_user(id):
    user = Utilisateur.query.get_or_404(id)
    data = request.get_json() or {}

    if 'email' in data and 'password' in data:
        user.email = data['email']
        user.password = generate_password_hash(data['password'])
    else:
        return jsonify({'message':'Le utilisateur non existant.'}), 404



@utilisateur_bp.route('/utilisateur/modifier-mot-de-passe', methods=["GET"])
def modifier_mot_de_passe():
    """Modifier de l'utilisateur"""
    pass


