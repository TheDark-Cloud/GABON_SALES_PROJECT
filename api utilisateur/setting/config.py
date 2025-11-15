from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import re


db: SQLAlchemy = SQLAlchemy()
SIMPLE_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def hpw(password):
    """Hash a password."""
    return generate_password_hash(password, method="sha256")


def is_valid_format(email: str) -> bool:
    """Check if the email is valid format."""
    return bool(SIMPLE_RE.match(email))
