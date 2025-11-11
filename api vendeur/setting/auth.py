from typing import Optional, Tuple, Dict, Any
from flask import Response, jsonify

ErrorResp = Tuple[Dict[str, Any], int]

def authenticate_validator(identity: Any = None, claims: Any = None) -> Optional[ErrorResp]:
    if identity is None or claims is None:
        return {"error": "Authorisation required"}, 401

    if not isinstance(identity, dict) or not isinstance(claims, dict):
        return {"error": "Invalid authorisation format"}, 400

    return None


def payload_validator(payload: Any, required_fields: Optional[list] = None) -> Optional[ErrorResp]:
    if payload is None:
        return {"error": "Empty data provided"}, 404

    if not isinstance(payload, dict):
        return {"error": "Invalid payload format; expected JSON object"}, 400

    if required_fields is not None:
        missing = [k for k in required_fields if k not in payload]
        if missing:
            return {"error": f"Missing required fields: {missing}"}, 400

    return None