from email.mime import image
import base64
from flask import Blueprint, jsonify, request
from setting.config import db
from setting.auth import authenticate_validator, payload_validator
from model_db import Product, Vendeur, Categorie, Boutique
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


add_product_bp = Blueprint('add_product', __name__)

@add_product_bp.route('/vendeur/add_product', methods=['POST'])
@jwt_required()
def add_product():
    """Adding a new product from a vendor in the database """
    identity = int(get_jwt_identity())
    claims = get_jwt()

    payload = request.get_json()
    required_fields = ["product_name", "price", 'image', "description", "quantity", "categorie_name"]

    try:
        image_b64 = payload.get('image')
        if image_b64 is None:
            image_data = b''
        else:
            image_data = base64.b64decode(image_b64)
    except ValueError:
        return jsonify({"error": "Invalid image format"}), 400

    authenticate_validator(identity= identity, claims=claims)
    payload_validator(payload, required_fields)

    boutique = Boutique.query.filter_by(id_boutique=claims.get('id_boutique'),
                                        id_vendeur=claims.get('id_vendeur')).first()
    if not boutique:
        return jsonify({"error": "Shop access does not exist, Access denied!"}), 403

    categorie = Categorie.query.filter_by(categorie_name=payload.get("categorie_name")).first()
    if not categorie:
        return jsonify({"error": "Categorie does not exist"}), 404
    try:

        if claims.get('name_role') == 'vendeur':
            product = Product(id_vendeur=boutique.id_vendeur,
                              id_categorie=categorie.id_categorie,
                              product_name=payload.get("product_name"),
                              price=payload.get("price"),
                              description=payload.get("description"),
                              quantity=payload.get("quantity"),
                              image=image_data)

            db.session.add(product)
            db.session.commit()
            print(boutique.to_dict())
            return jsonify({"error": "Product added successfully",
                            "data": product.to_dict()}), 201

        else:
            db.session.rollback()
            return jsonify({"error": "Unauthorized Access"}), 403

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500

