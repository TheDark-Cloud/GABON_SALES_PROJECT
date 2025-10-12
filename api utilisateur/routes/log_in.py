from flask import Blueprint, request, jsonify, session
from model_db import Utilisateur
from extension import db

log_in_bp = Blueprint('log_in', __name__, url_prefix='/log_in')

@log_in_bp.route('/log_in', methods=['POST'])
def account_login():
    data = request.get_json()
    use = Utilisateur.query.filter_by(identite=data['email']).first()
    if not use:

    pass