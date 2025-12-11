from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from model_db import Product
from setting.auth import authenticate_validator, payload_validator
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

        authenticate_validator(identity, claims)
        payload_validator(payload, required_fields)


        try:
            if claims.get('role') == 'Vendeur':
                id_product = identity["id_vendeur"]
                id_vendeur = identity["id_vendeur"]

                my_product = Product.query.filter_by(id_product=id_product, id_vendeur=id_vendeur).first()
                if my_product == 0:
                    db.session.rollback()
                    return jsonify({"error": "Product not found"}), 404

                my_product.name = payload.get("product_name")
                my_product.price = payload.get("price")
                my_product.description = payload.get("description")
                my_product.quantity = payload.get("quantity")
                my_product.image = payload.get("image")
                db.session.commit()
                db.session.close()
                return jsonify({"message": "Product updated successfully"}), 200

        except Exception as ex:
            db.session.rollback()
            return jsonify({"error": str(ex)}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

