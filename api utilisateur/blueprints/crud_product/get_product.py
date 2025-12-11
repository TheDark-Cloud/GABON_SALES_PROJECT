from flask import jsonify, request, Blueprint
from setting.auth import authenticate_validator, payload_validator
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from model_db import Product

get_product_bp = Blueprint('get_product', __name__)

@get_product_bp.route('/get_product', methods=['GET'])
@jwt_required()
def get_product():
    """Return all the product of a user"""

    identity = get_jwt_identity()
    claims = request.get_json()

    authenticate_validator(identity, claims)

    try:
        if claims.get('name_role') != 'vendeur':
            return jsonify({"error": "Unauthorized access"}), 403

        products = Product.query.filter_by(id_vendeur=identity['id_vendeur']).all()
        if not products:
            return jsonify({"error": "Product not found"}), 404
        return jsonify({"products": [product.to_dict() for product in products]}), 200

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500