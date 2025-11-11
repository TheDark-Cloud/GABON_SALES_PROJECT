from flask import Blueprint, request, jsonify
from model_db import Categorie
from setting.config import db
from flask_jwt_extended import jwt_required, get_jwt
from setting.auth import authenticate_validator, payload_validator

add_categorie_bp = Blueprint('add_categorie', __name__)

@add_categorie_bp.route('/add_categorie', methods=['POST'])
@jwt_required()
def add_category():
    """Add categories in the database"""
    claims = get_jwt()
    payload = request.get_json()

    if authenticate_validator(claims):
        try:
            if claims.get('role') == 'Admin':
                if payload_validator(payload):

                    if Categorie.query.filter_by(nom_categorie=payload['nom_categorie']).scalar() is not None:
                        return jsonify({"error":"Category already exist"}), 409

                    categorie = Categorie(nom_categorie=payload['nom_categorie'])
                    db.session.add(categorie)
                    db.session.commit()
                return jsonify(categorie.to_dict()), 201

        except Exception as ex:
            db.session.rollback()
            return ({"error": str(ex)}), 404


    return jsonify({"error": "Unauthorized role"}), 403