from flask import Blueprint, jsonify, request
from model_db import Vendeur
from extension import db
from flask_jwt_extended import create_access_token


vendeur_bp = Blueprint('vendeur', __name__, url_prefix='/vendeur')

@vendeur_bp.route('/vendeur', methods=['GET'])
def create_vendeur():
    new_vendor = request.get_json() or {}
    pass


