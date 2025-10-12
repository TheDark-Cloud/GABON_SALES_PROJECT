from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from extension import db
from model_db import Administrateur, Utilisateur, Vendeur

admin_bp = Blueprint('admin', __name__)

def admin_required(fn):
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get('is_admin') is not True:
            return jsonify({'error': 'Admin only'}), 403
        return fn(*args, **kwargs)
    wrapper.__name__ = fn.__name__
    return wrapper

@admin_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@admin_required
def list_users():
    users = Utilisateur.query.all()
    return jsonify([u.serialize() for u in users]), 200

@admin_bp.route('/admin/vendeurs', methods=['GET'])
@jwt_required()
@admin_required
def list_vendeurs():
    vendeurs = Vendeur.query.all()
    return jsonify([v.serialize() for v in vendeurs]), 200