from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from model_db import Boutique
from setting.config import db
from setting.auth import authenticate_validator, payload_validator

add_shop_bp = Blueprint('add_shop', __name__)

@add_shop_bp.route('/add_shop', methods=['POST'])
@jwt_required()
def add_shop():
    """Add a shop in the database"""
    claims = get_jwt()
    identity = get_jwt_identity()

    authenticate_validator(None,claims=claims)

    payload = request.get_json()
    required_fields = ['name', 'address', 'phone', 'email']

    payload_validator(payload, required_fields)


    if claims.get('role') != 'Vendeur':
        return jsonify({"error": "Unauthorized role"}), 403
    try:
        shop = Boutique(id_vendeur=identity['id_vendeur'],
                        name=payload['name'],
                        address=payload['address'],
                        domaine=payload['domaine'],
                        description=payload['description'])
        db.session.add(shop)
        db.session.commit()
        return jsonify({"error": "Shop added successfully",
                        "data": shop.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500