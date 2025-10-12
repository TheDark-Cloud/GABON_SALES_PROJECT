from flask import Blueprint, jsonify

from extension import db
from model_db import Role


role_bp = Blueprint('role', __name__)

# pour l'inscription utilisateur
@role_bp.route('/role', methods=['GET'])
def get_role():
    try:
        roles = db.session.query(Role).filter(Role.id != 1).all()
        print(roles)
        return jsonify([role.to_dict() for role in roles])
    except Exception as e:
        print(e)
