from flask import Blueprint, jasonify, request, jsonify
from model_db import Utilisateur
from extension import db
import re

utilisateur_bp = Blueprint('utilisateur', __name__, url_prefix='/utilisateur')


@utilisateur_bp.route('/', methods=['GET'])
def index():
    pass


# Creation des comptes

@utilisateur_bp.route('/', methods=['POST'])
def create_user():
    """Creation de l'utilisateur avec selection du role"""

    new_user = request.get_json() or {}

    email = new_user.get('email')
    password = new_user.get('password')
    id_role = new_user.get('id_role')

    if not email or not password or not id_role:
        return jsonify({"error":"Veuillez entrez tous les champs."}), 404

    # Entry validation



    if Utilisateur.query.filter_by(email=email).first():
        return jsonify({'error':"L'addresse email existe deja"}), 409

    # sending the data in the database
    try:
        user = Utilisateur(email, password, id_role)
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify({"error":str(e)}), 500

    return jsonify({'user':user.to_dict()}), 201




