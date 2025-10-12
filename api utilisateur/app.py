from flask import Flask
from extension import db, JWT_SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from blueprints.role import role_bp
from blueprints.utilisateur import utilisateur_bp
from blueprints.complete_compte import complete_compte_bp
from blueprints.role import role_bp
from blueprints.log_in import log_in_bp
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = JWT_SECRET_KEY

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
