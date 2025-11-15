from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import jsonify, Blueprint, request
from model_db import Utilisateur
from setting.config import db

update_user_bp = Blueprint("update_user", __name__)

@update_user_bp.route("/update_user", methods=["PUT"])
@jwt_required()
def update_user():
    pass
