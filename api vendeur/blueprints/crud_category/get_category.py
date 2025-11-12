from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt, jwt_required
from model_db import Categorie
from setting.auth import authenticate_validator

get_categorie_bp = Blueprint('get_categorie', __name__)

@get_categorie_bp.route('/get_categorie', methods=['GET'])
@jwt_required()
def get_categorie():
    """Return a library of all the categories"""
    claims = get_jwt()
    authenticate_validator(claims=claims)
    if claims.get('role') != 'Admin':
        return jsonify({"error": "Unauthorized role"}), 403
    try:
        categories = Categorie.query.all()
        if not categories:
            return jsonify({"error": "No categories found"}), 204

        return jsonify({"data": [categorie.to_dic() for categorie in categories]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
