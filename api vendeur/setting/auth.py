from functools import wraps
from flask import current_app, request, jsonify
from token_jwt import decode_token

def _token_extraction():
    """Extraction of the header {"Authorisation": "Bearer <token>"}
    It sends a request to get and validate the header"""
    current_app_header_name = current_app.config.get("JWT_HEADER_NAME")
    current_app_header_type = current_app.config.get("JWT_HEADER_TYPE")

    # sending a request to get the header and comparing it with that of the application
    header = request.headers.get(current_app_header_name, "")

    if not header: # checking if the header is not an empty object
        # the format should match that of the application
        return None, jsonify({"error": {"message": "Invalid Authorization header"}}), 401
        # 401 unauthorize error

    # splitting the header into header_type and toke
    header_value = header.split()

    if len(header_value) != 2 or header_value[0].lower() != current_app_header_type.lower():
        return None, jsonify({"error":{"message":"Invalid Authorisation header format"}}), 401

    # Now checking the token
    token = header_value[1].strip()
    if not token or not isinstance(token, str): # check if that the token is a non-empty string
        return None, jsonify({"error":{"message":"Empty Token"}}), 401

    return token, None

# Making the decorator that will retrieve and validate the token and decode it before applying to the route
def token_required(fn):
    """1 - Extract the token
        2 - Validate the header and decode the token
        3 - Inject it into the route function as a parameter"""
    @wraps(fn)
    def decorated(*args, **kwargs):
        token, error = _token_extraction()
        if error: return error

        try:
            payload = decode_token(token)
        except ValueError as e:
            return jsonify({"error":{"message":str(e)}}), 401
        kwargs["_token"] = payload
        return fn(*args, **kwargs)
    return decorated



# function to decode passwords

def unhashed_password(password) -> str:
    return password