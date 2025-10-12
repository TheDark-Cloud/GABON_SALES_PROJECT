from flask import Blueprint, jsonify, request
from model_db import Vendeur, Client
from extension import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

comple_compte_bp = Blueprint('complete_compte', __name__)

@comple_compte_bp.route('/comple_compte/<int:id>', methods=['POST'])
@jwt_required
def create_vendeur(id):
    """Cpompleting either Vendeur or Client account"""
    caller_id = get_jwt_identity()
    claims = get_jwt()

    if claims.get('scope') != 'onboarding':
        return jsonify({'error':'Token scope invalide'})
    if caller_id != id:
        return jsonify({"error":"Token UID mismatch "}), 403

    id_role = claims.get('id')

    data = request.get_json() or {}
    nom = data.get('nom')
    prenom = data.get('prenom')
    numero = data.get('numero')
    identite = data.get('identite')

    match id_role:
        case '2': # for vendor
            try:
                new_vendeur = Vendeur(nom=nom, prenom=prenom, numero=numero, identite=identite)
                db.session.add(new_vendeur)
                db.session.commit()
                return jsonify({'message':'Votre compte vendeur a ete complete avec succes'}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': str(e)}), 403

        case '3': # for client
            try:
                new_client = Client(nom=nom, prenom=prenom, numero=numero)
                db.session.add(new_client)
                db.session.commit()
                return jsonify({'message': 'Votre compte client a ete complete avec succes'}), 201
            except Exception as e:
                db.session.rollback()
                return jsonify({'error':str(e)}), 403

