from flask import Blueprint, jsonify, current_app
from sqlalchemy.exc import SQLAlchemyError
from extension import db
from model_db import Role

role_bp = Blueprint("role", __name__, url_prefix="/roles")

@role_bp.route("", methods=["GET"])
def get_roles():
    try:
        roles = db.session.query(Role).filter(Role.id_role != 1).all()
        return jsonify({"data": [r.to_dict() for r in roles]}), 200
    except SQLAlchemyError:
        current_app.logger.exception("Failed to fetch roles")
        return jsonify({"error": {"message": "Internal server error"}}), 500