from flask import Blueprint, jsonify

from extension import db
from model_db import Role


role_bp = Blueprint('role', __name__)

# pour l'inscription utilisateur
@role_bp.route('/role', methods=['GET'])
def get_role():
    print("role")
    # roles = db.session.query(Role).all()
    try:
        #roles = Role.query.all()
        roles = db.session.query(Role).all()
        print(roles)
        return jsonify([role.to_dict() for role in roles])
    except Exception as e:
        print(e)
