from flask_sqlalchemy import SQLAlchemy
import os
from datetime import timedelta

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "cVUGtw10B_PRv2jaCS1IUbzxnucRIJ79fMQ4dGhUEUw")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:Admin@localhost:5433/api_utilisateur_db")
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_ALGORITHM = "HS256"



db = SQLAlchemy()


