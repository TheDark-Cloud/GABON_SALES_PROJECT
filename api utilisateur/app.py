import os

from flask import Flask
from extension import db
from blueprints.role import role_bp
from blueprints.utilisateur import utilisateur_bp
from blueprints.complete_compte import complete_compte_bp
from blueprints.role import role_bp
from blueprints.log_in import log_in_bp
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from os import getenv
from dotenv import load_dotenv

from model_db import Role

migrate = Migrate()

load_dotenv()
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config["JWT_ALGORITHM"] = os.environ.get('JWT_ALGORITHM')
    app.config["JWT_HEADER_TYPE"] = os.environ.get('JWT_HEADER_TYPE')
    app.config["JWT_HEADER_TYPE"] = os.environ.get('JWT_HEADER_TYPE')

    db.init_app(app)
    jwt = JWTManager(app)
    migrate.init_app(app, db)
    app.register_blueprint(utilisateur_bp)
    app.register_blueprint(complete_compte_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(log_in_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    try:
        with app.app_context():
            db.create_all()

    except Exception as e:
        print(e)
    app.run(debug=True, port=5000)
