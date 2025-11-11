from typing import Optional, Tuple

def authenticate_validator(identity=None, claims=None) -> Tuple[bool, Optional[str]]:
    if identity is None or claims is None:
        return False, "Authorisation required"

    if not isinstance(identity, dict) or not isinstance(claims, dict):
        return False, "Invalid authorisation format"

    return True, None


def payload_validator(payload, required_fields: Optional[list] = None) -> Tuple[bool, Optional[str]]:
    if payload is None:
        return False, "Empty data provided"

    if not isinstance(payload, dict):
        return False, "Invalid payload format; expected JSON object"

    if required_fields:
        missing = [k for k in required_fields if k not in payload]
        if missing:
            return False, f"Missing required fields: {missing}"

    return True, None