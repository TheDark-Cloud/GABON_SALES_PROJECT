from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from model_db import Product
from setting.config import db


delete_product_bp = Blueprint('delete_product', __name__)

@delete_product_bp.route('/delete_product', methods=['DELETE'])
@jwt_required()
def delete_product():
    """Delete a product from the database"""
    identity = get_jwt_identity()
    claims = get_jwt()


    if not identity or not claims:
        return jsonify({"error": "Authorisation required"}), 401

    id_product = identity if isinstance(identity, int) else identity["id_product"]
    id_vendeur = claims.get('id_vendeur')

    try:
        row = Product.query.filter_by(id_product=id_product, id_vendeur=id_vendeur).delete()
        if row == 0:
            db.session.rollback()
            return jsonify({"error": "Product not found"}), 404

        db.session.commit()
        return jsonify({"message": "Product deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500