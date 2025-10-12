from flask import Blueprint, request, jsonify, session
from model_db import Utilisateur
from extension import db

log_in_bp = Blueprint('log_in', __name__)

@log_in_bp.route('/log_in', methods=['POST'])
def account_login():
    pass