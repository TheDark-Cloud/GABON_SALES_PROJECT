from flask import Blueprint, request, jsonify
from setting.config import db
from model_db import Product
from setting.auth import token_required, decode_token


add_produit_bp = Blueprint('add_produit', __name__)

@add_produit_bp.route('/add_product', methods=['POST'])
@token_required
def add_produit(token: str):
    """Adding a new product from a vendor in the database """
    current_user = decode_token(token)

    required_fields = ['role', 'id_vendeur', 'product_name', 'price', 'description', 'quantity', 'image']
    if not all(fields in current_user for fields in required_fields):
        return jsonify({"error": {"message": "Missing required fields"}}), 400

    try:
        if current_user['role'] == 'vendeur':
            product = Product(id_vendeur=current_user['id_vendeur'],
                              product_name=current_user["product_name"],
                              price=current_user["price"],
                              description=current_user["description"],
                              quantity=current_user["quantity"],
                              image=current_user["image"])

            db.session.add(product)
            db.session.commit()
            return jsonify({"message": "Product added successfully"}), 201

        else:
            db.session.rollback()
            return jsonify({"message": "Unauthorized role"}), 401

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

