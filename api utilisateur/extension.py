# """Shared extensions used by the Flask application."""
# from flask_sqlalchemy import SQLAlchemy
# db: SQLAlchemy = SQLAlchemy()
#
#
# import jwt
# from datetime import datetime, timedelta
# from flask import current_app
#
# def generate_token(identity: dict):
#     info = {
#         "sub": str(identity.get("id_utilisateur")),              # Subject of the token
#         "iat": datetime.utcnow(),                # Issued at
#         "exp": datetime.utcnow() + timedelta(days=365*80)  # Expiration
#     }
#
#     payload = {**info, **identity}
#
#     token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
#     return token
#
# def decode_token(token):
#     try:
#         payload = jwt.decode(
#             token,
#             current_app.config["SECRET_KEY"],
#             algorithms=["HS256"]
#         )
#         return payload  # This will be a dict with your claims
#     except jwt.ExpiredSignatureError:
#         return {"error": "Token has expired"}
#     except jwt.InvalidTokenError:
#         return {"error": "Invalid token"}


"""Shared extensions used by the Flask application."""
from flask_sqlalchemy import SQLAlchemy
db: SQLAlchemy = SQLAlchemy()

import jwt
from datetime import datetime, timedelta
from flask import current_app

# extension.py (token parts)

import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app

def _now_utc_ts() -> int:
    return int(datetime.now(timezone.utc).timestamp())

def _ts_from_delta(delta: timedelta) -> int:
    return int((datetime.now(timezone.utc) + delta).timestamp())

def generate_token(identity: dict, expires_delta: timedelta | None = None) -> str:
    if not isinstance(identity, dict):
        raise TypeError("identity must be a dict")
    key = current_app.config.get("SECRET_KEY")
    if not key:
        raise RuntimeError("SECRET_KEY is not configured")

    now_ts = _now_utc_ts()
    # default to 50 years
    expires_delta = expires_delta if expires_delta is not None else timedelta(days=365 * 50)
    exp_ts = _ts_from_delta(expires_delta)

    payload = {
        "sub": str(identity.get("id_utilisateur")),
        "iat": now_ts,
        "exp": exp_ts,
        **identity
    }

    token = jwt.encode(payload, key, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token

def decode_token(token: str) -> dict:
    key = current_app.config.get("SECRET_KEY")
    if not key:
        raise RuntimeError("SECRET_KEY is not configured")

    try:
        # add a small leeway to avoid tiny clock skew issues
        payload = jwt.decode(token, key, algorithms=["HS256"], options={"require": ["exp", "iat"]}, leeway=10)
        if not isinstance(payload, dict):
            raise ValueError("Decoded token payload is not a dict")
        return payload
    except jwt.ExpiredSignatureError as exc:
        current_app.logger.info("Token expired: %s", exc)
        raise ValueError("Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        current_app.logger.info("Invalid token: %s", exc)
        raise ValueError("Invalid token") from exc