from flask import jsonify

def authenticate_validator(identity=None, claims=None) :
    if identity is None or claims is None:
        return jsonify({"error":"Invalid authorisation required"}), 401

    if not isinstance(identity, dict) or not isinstance(claims, dict):
        return jsonify({"error":"Invalid authorisation format"}), 400

    return None


def payload_validator(payload, required_fields = None):
    if payload is None:
        return jsonify({"error": "Empty data provided"}), 400

    if not isinstance(payload, dict):
        return jsonify({"error": "Invalid payload format; expected JSON object"}), 400

    if required_fields is not None:
        missing = [k for k in required_fields if k not in payload]
        if missing:
            return jsonify({"error": f"Missing required fields: {missing}"}), 400

    return None