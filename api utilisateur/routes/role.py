from flask import Blueprint, jsonify

from extension import db
from model_db import Role


role_bp = Blueprint('role', __name__)

@role_bp.route('/role', methods=['POST'])
def get_role():
    roles = db.session.query(Role).all()
    return jsonify([role.serialize() for role in roles])