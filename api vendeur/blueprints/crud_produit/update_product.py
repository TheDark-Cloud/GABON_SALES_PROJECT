from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from model_db import Product
from setting.config import db


update_product_bp = Blueprint('update_product', __name__)

@update_product_bp.route('/update_product', methods=['PUT'])
@jwt_required()
def update_product():
    """Updating a product in the database"""
    try:
        claims = get_jwt()
        identity = get_jwt_identity()

        payload = request.get_json()
        required_fields = ['id_vendeur', 'product_name', 'price', 'description', 'quantity', 'image']

        if not claims or not identity:
            return jsonify({"error": "Authorisation required"}), 401
        if not payload:
            return jsonify({"error": "Emmpty data provided"}), 204
        if not isinstance(payload, dict):
            return jsonify({"error": "Invalid payload"}), 400

        if not all(k in payload for k in required_fields):
            return jsonify({"error": "Missing required fields"}), 400


        try:
            if claims.get('role') == 'Vendeur':
                id_product = identity["id_vendeur"]
                id_vendeur = identity["id_vendeur"]

                row = Product.query.filter_by(id_product=id_product, id_vendeur=id_vendeur).update({"product_name": payload['product_name'],
                                                                       "price": payload['price'],
                                                                       "description": payload['description'],
                                                                       "quantity": payload['quantity'],
                                                                       "image": payload['image']})
                if row == 0:
                    db.session.rollback()
                    return jsonify({"error": "Product not found"}), 404

                db.session.commit()
                db.session.close()
                return jsonify({"message": "Product updated successfully"}), 200

        except Exception as ex:
            db.session.rollback()
            return jsonify({"error": str(ex)}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

