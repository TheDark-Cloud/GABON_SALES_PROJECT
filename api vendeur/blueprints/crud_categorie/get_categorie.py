from flask import Blueprint, jsonify

from model_db import Categorie
from setting.config import db


get_categorie_bp = Blueprint('get_categorie', __name__)

# this route is ok
@get_categorie_bp.route('/get_categorie', methods=['GET'])
def get_categorie():
    """Return a library of all the categories"""
    try:
        categories = Categorie.query.all()
        if not categories:
            return jsonify({"error": "No categories found"}), 204

        return jsonify({"data": [categorie.to_dic() for categorie in categories]}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
