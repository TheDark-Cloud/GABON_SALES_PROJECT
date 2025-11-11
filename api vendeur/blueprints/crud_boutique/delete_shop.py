from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from model_db import Boutique
from setting.config import db
from setting.auth import authenticate_validator


delete_shop_bp = Blueprint("delete_shop", __name__)

@delete_shop_bp.route('/delete_shop', methods=['DELETE'])
@jwt_required()
def delete_shop():
    """Removes a shop from the database"""

    identity = get_jwt_identity()
    authenticate_validator(identity)

    try:
        if Boutique.query.filter_by(id_vendeur=identity['id_vendeur'], id_boutique=identity['id_vendeur']).delete()==0:
            return jsonify({"error": "Shop not found"}), 404
        db.session.commit()
        return jsonify({"message": "Shop removed successfully"}), 203
    except Exception as e:
        return jsonify({"error": str(e)}), 500
