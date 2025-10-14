import jwt
import time
from flask import current_app

class TokenError(Exception):
    pass

def create_encoded_token(identity: dict, expire: int = None, algorithm: str = None) -> str:
    """Generate JWT token
    Args: identity (dict), expiration(int: if given int(os.getenv("JWT_EXP_DELTA_SECONDS"="2524608000")
    return token (str) encoded by jwt
    """
    now = int(time.time()) # setting the ime of creation
    expire = expire or current_app.config.get("JWT_EXP_DELTA_SECONDS") # setting the expiration time

    payload = {"iat": now,"exp": now + expire}
    # iat for issued at time()...
    # exp for expiry time()...
    payload.update(identity) # adding the information dictionary to the payload

    key = current_app.config.get("JWT_SECRET_KEY")
    alg = algorithm or current_app.config.get["JWT_ALGORITHM"]

    token = jwt.encode(payload, key, algorithm=alg) # encoding all the sensitive information

    return token

def decode_token(token: str) -> dict:
    """Decode JWT token
    Args: token(str): JWT token"""
    key = current_app.config.get(["JWT_SECRET_KEY"]) # must be the key used to encode the token
    alg = current_app.config.get("JWT_ALGORITHM")

    if not token or not isinstance(token, str): # check if that the token is a non-empty string
        raise TokenError("Token Class Error")

    try:
        payload = jwt.decode(token, key, algorithms=[alg])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token Expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid Token")