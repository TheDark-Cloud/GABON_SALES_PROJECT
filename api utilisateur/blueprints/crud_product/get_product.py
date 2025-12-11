from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from model_db import Product, Categorie
from setting.auth import authenticate_validator

get_product_bp = Blueprint("get_product", __name__)

@get_product_bp.route("/product/get_products", methods=["GET"])
@jwt_required()
def get_products():
    identity = int(get_jwt_identity())
    claims = get_jwt()
    authenticate_validator(identity=identity, claims=claims)
    if not claims.get("is_complete"):
        return jsonify({"error": "Unauthorized access. Uncompleted user"}), 401

    role = claims.get("name_role")
    id_vendeur = claims.get("id_vendeur")

    # Optional filters
    filters = request.args
    product_name = filters.get("product_name")
    category_name = filters.get("category_name")

    query = Product.query

    if role == "vendeur":
        query = query.filter_by(id_vendeur=id_vendeur)

    if category_name:
        category = Categorie.query.filter_by(categorie_name=category_name).first()
        if not category:
            return jsonify({"error": "Category not found"}), 404
        query = query.filter_by(id_categorie=category.id_categorie)

    if product_name:
        query = query.filter(Product.product_name.ilike(f"%{product_name}%"))

    products = query.all()

    result = []
    for p in products:
        result.append({
            "id_product": p.id_product,
            "product_name": p.product_name,
            "price": float(p.price),
            "description": p.description,
            "quantity": p.quantity,
            "image": p.to_dict().get("image"),
            "categorie_name": p.categorie.categorie_name if p.categorie else None,
            "vendor_id": p.vendeur.id_vendeur
        })

    return jsonify({"products": result}), 200