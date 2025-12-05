import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import re
from flask import jsonify, Response

db: SQLAlchemy = SQLAlchemy()
SIMPLE_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def hpw(password):
    """Hash a password."""
    return generate_password_hash(password, method=os.environ.get("JWT_ALGORITHM_HPW"))

def is_valid_password_format(password):
    """Check if the password is valid."""
    if not isinstance(password, str) and len(password) < 8:
        return False
    return True

def is_valide_phone_format(phone_number):
    """Check if the password is valid."""
    if not isinstance(phone_number, str):
        return False
    if phone_number != 9:
        return False
    return True

def is_valid_email_format(email: str) -> Response | bool:
    """Check if the email is in valid format."""
    if not email or email == "":
        return jsonify({"error": "The mail should not be empty"})
    return bool(SIMPLE_RE.match(email))

def validate_parameters(mail, password, phone_number):
    if not is_valide_phone_format(phone_number):
        return jsonify({"message": "Invalid phone number"}), 400

    if not is_valid_email_format(mail):
        return jsonify({"message": "Invalid email"}), 400

    if not is_valid_password_format(password):
        return jsonify({"message": "Invalid password"}), 400
    return True