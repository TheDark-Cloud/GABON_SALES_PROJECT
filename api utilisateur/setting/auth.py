from typing import Optional, Tuple, Dict, Any

from flask import jsonify, Response

ErrorResp = Tuple[Dict[str, Any], int]

def authenticate_validator(identity: int, claims: Any = None) -> tuple[Response, int] | tuple[
    dict[str, str], int] | None:
    if identity is None:
        return jsonify({"error": "Missing identity data"}), 400
    if claims is None:
        return jsonify({"error": "Authorisation required"}), 401

    if not isinstance(identity, int) or not isinstance(claims, dict):
        return jsonify({"error": "Invalid authorisation format"}), 400

    return None


def payload_validator(payload: Any = None, required_fields: Optional[list] = None):
    if payload is None:
        return jsonify({"error": "Empty data provided"}), 404
    if not isinstance(payload, dict):
        return jsonify({"error": "Invalid payload format; expected JSON object"}), 400

    missing = [k for k in required_fields if k not in payload]
    if missing:
        return {"error": f"Missing required fields: {missing}"}, 400
    for k in required_fields:
        value = payload.get(k)

        if value is None:
            return {"error": f"Missing required field: {k}"}, 400

        if not isinstance(value, str):
            return {"error": f"Field '{k}' must be a string"}, 400

        if not value.strip():
            return {"error": f"Field '{k}' cannot be empty"}, 400

    return None


