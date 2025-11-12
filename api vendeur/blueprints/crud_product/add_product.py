from flask import Blueprint, jsonify, request
from setting.config import db
from setting.auth import authenticate_validator, payload_validator
from model_db import Product
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


add_product_bp = Blueprint('add_product', __name__)

@add_product_bp.route('/add_product', methods=['POST'])
@jwt_required()
def add_product():
    """Adding a new product from a vendor in the database """

    identity = get_jwt_identity()
    claims = get_jwt()

    payload = request.get_json()
    required_fields = ["product_name", "price", "description", "quantity", "image"]

    authenticate_validator(identity, claims)
    payload_validator(payload, required_fields)

    try:
        if claims.get('role') == 'Vendeur':
            id_vendeur = identity if isinstance(identity, int) else identity["id_vendeur"]

            product = Product(id_vendeur=id_vendeur,
                              product_name=payload["product_name"],
                              price=payload["price"],
                              description=payload["description"],
                              quantity=payload["quantity"],
                              image=payload["image"])

            db.session.add(product)
            db.session.commit()
            return jsonify({"error": "Product added successfully",
                            "data": product.to_dict()}), 201

        else:
            db.session.rollback()
            return jsonify({"error": "Unauthorized role"}), 403

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

