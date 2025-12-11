from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from model_db import Boutique
from setting.config import db
from setting.auth import authenticate_validator, payload_validator

update_shop_bp = Blueprint("update_shop", __name__)

@update_shop_bp.route('/update_shop', methods=['PUT'])
@jwt_required()
def update_shop():
    """Update a shop in the database"""
    identity = get_jwt_identity()
    authenticate_validator(identity)

    payload = request.get_json()
    required_fields = ['name', 'address', 'domain', 'description']

    payload_validator(payload, required_fields)

    try:
        row = Boutique.query.filter_by(id_boutique=identity['id_boutique']).update({"name": payload['name'],
                                                                                    "address": payload['address'],
                                                                                    "domaine": payload['domaine'],
                                                                                    "description": payload['description']})
        if row == 0:
            return jsonify({"error": "Shop not found"}), 404
        db.session.commit()
        return jsonify({"message": "Shop updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


