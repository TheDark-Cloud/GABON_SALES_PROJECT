"""Shared extensions used by the Flask application."""
from flask_sqlalchemy import SQLAlchemy
db: SQLAlchemy = SQLAlchemy()


import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_token(identity):
    info = {
        "sub": str(identity.id_utilisateur),              # Subject of the token
        "id": identity.id_utilisateur,               # Explicit ID claim
        "iat": datetime.utcnow(),                # Issued at
        "exp": datetime.utcnow() + timedelta(days=365*80)  # Expiration
    }

    payload = {**info, **identity}

    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token):
    try:
        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
        return payload  # This will be a dict with your claims
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}