from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from model_db import Categorie
from setting.config import db

add_categorie_bp = Blueprint('add_categorie', __name__)

# this route is ok
@add_categorie_bp.route('/add_categorie', methods=['POST'])
def add_category():
    """Add categorie in the databse"""
    data = request.get_json()

    try:
        if not data:
            return jsonify({"error":{"message": "Empty data provided"}}), 204

        name = data['nom_categorie']

        if db.session.query(Categorie).filter(Categorie.nom_categorie == name).scalar():
            return jsonify({"error":{"message": "Category already exist"}}), 409
        categorie = Categorie( nom_categorie=name)
        db.session.add(Categorie(nom_categorie =name))
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return ({"error":{"message": "Category already exist"}}), 409
    return jsonify(categorie.to_dict()), 201

