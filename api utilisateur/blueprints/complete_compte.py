import json

import jwt
from flask import Blueprint, jsonify, request
from model_db import Vendeur, Client
from extension import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request

complete_compte_bp = Blueprint('complete_compte', __name__)

@complete_compte_bp.route('/complete_compte', methods=['POST'])
@jwt_required()
def create_vendeur():
    eb = request.headers.get('Authorization')
    print(eb)
    """Cpompleting either Vendeur or Client account"""
    try:
        verify_jwt_in_request()
        caller_id = get_jwt_identity()
        user = json.loads(caller_id)
        if user.get("id_role")!= 2:
            print(" 403")

        id_utlisateur = user.get("id_utlisateur")

    except jwt.JWTError as e:
        print(e)
    id_role = user.get("id_role")
    match id_role:
        case '2': # for vendor
            try:
                data = request.get_json() or {}
                nom = data.get('nom')
                prenom = data.get('prenom')
                numero = data.get('numero')
                identite = data.get('identite')
                id_utilisateur = caller_id

                new_vendeur = Vendeur(nom=nom, prenom=prenom, numero=numero, identite=identite, id_utilisateur=id_utilisateur)
                db.session.add(new_vendeur)
                db.session.commit()
                return jsonify({'message':'Votre compte vendeur a ete complete avec succes'}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 403

        case '3': # for client
            try:
                data = request.get_json() or {}
                nom = data.get('nom')
                prenom = data.get('prenom')
                numero = data.get('numero')
                id_utilisateur = caller_id

                new_client = Client(nom=nom, prenom=prenom, numero=numero, id_utilisateur=id_utilisateur)
                db.session.add(new_client)
                db.session.commit()
                return jsonify({'message': 'Votre compte client a ete complete avec succes'}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error':str(e)}), 403

