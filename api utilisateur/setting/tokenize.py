from datetime import timedelta

from flask import current_app
from flask_jwt_extended import create_access_token


def tokenize(identity: dict, claims: dict, expire = None):
    exp = expire or int(current_app.config.get("JWT_EXP_DELTA_SECONDS"))
    # setting the expiration time

    token = create_access_token(identity=identity,additional_claims=claims,
                                expires_delta=timedelta(seconds=exp))
    return token

