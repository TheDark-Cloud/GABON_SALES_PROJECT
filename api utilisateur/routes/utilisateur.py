from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from model_db import Utilisateur, Role
from extension import db

utilisateur_bp = Blueprint('utilisateur', __name__)


# Creation des comptes
@utilisateur_bp.route('/utilisateur', methods=["POST"])
def create_user():
    """Creation de l'utilisateur avec selection du role"""

    data = request.get_json() or {}

    email = data.get('email')
    hsh_password = generate_password_hash(data.get('password'))
    nom_role = data.get('nom_role')

    if not all([email, hsh_password, nom_role]):
        return jsonify({"error":"email, mot_de_passe, role requis."}), 400

    # checking if the email is already in the database
    if Utilisateur.query.filter_by(email=email).first():
        return jsonify({'error':"L'addresse email existe deja"}), 409

    role= Role.query.filter_by(nom_role=data['nom_role']).first():
    if not role:
        return role.id_role
    id_role = role.id
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
    return jsonify({'message':'Compte cree avec succes',
                    'id_utilisateur': user.id,
                    'email': user.email,}), 201

# Lire un utilisateur
@utilisateur_bp.route('/utilisateur/<int:id>', methods=["GET"])
def get_user(id):
    user = Utilisateur.query.get_or_404(id)
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


