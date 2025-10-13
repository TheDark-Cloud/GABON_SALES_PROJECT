from flask import Blueprint, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from extension import db
from model_db import Administrateur, Utilisateur, Vendeur

ADMIN_CLAIM_KEY = "is_admin"
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        claims = get_jwt() or {}
        if not claims.get(ADMIN_CLAIM_KEY):
            return jsonify({"error": {"message": "Admin only"}}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route("/vendeurs/block/<int:vendeur_id>", methods=["PUT"])
@jwt_required()
@admin_required
def block_vendeur(vendeur_id):
    vendeur = Vendeur.query.get(vendeur_id)
    if not vendeur:
        return jsonify({"error": {"message": "Vendeur introuvable"}}), 404
    vendeur.statut = False
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Failed to block vendeur %s", vendeur_id)
        return jsonify({"error": {"message": "Internal server error"}}), 500
    return jsonify({"data": {"message": "Vendeur bloqué", "id": vendeur_id}}), 200

@admin_bp.route("/users", methods=["GET"])
@jwt_required()
@admin_required
def list_users():
    users = Utilisateur.query.all()
    return jsonify({"data": [u.to_dict() for u in users]}), 200

@admin_bp.route("/vendeurs", methods=["GET"])
@jwt_required()
@admin_required
def list_vendeurs():
    vendeurs = Vendeur.query.all()
    return jsonify({"data": [v.to_dict() for v in vendeurs]}), 200