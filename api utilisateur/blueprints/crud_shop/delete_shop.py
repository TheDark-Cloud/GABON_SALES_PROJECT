from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from model_db import Boutique
from setting.config import db
from setting.auth import authenticate_validator


delete_shop_bp = Blueprint("delete_shop", __name__)

@delete_shop_bp.route('/delete_shop', methods=['DELETE'])
@jwt_required()
def delete_shop():
    """Removes a shop from the database"""

    identity = get_jwt_identity()
    claims = get_jwt()
    authenticate_validator(identity, claims)

    try:
        boutique = Boutique.query.filter_by(id_vendeur=claims.get('id_vendeur')).first()
        if not boutique:
            return jsonify({"error": "Shop not found"}), 404
        boutique.status = False

        db.session.commit()
        return jsonify({"message": "Shop removed successfully"}), 203
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
