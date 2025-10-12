from flask import Flask
from extension import db, JWT_SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from routes.role import role_bp
from routes.utilisateur import utilisateur_bp
from routes.comple_compte import comple_compte_bp
from routes.role import role_bp
from routes.log_in import log_in_bp
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
    app.register_blueprint(utilisateur_bp, url_prefix='/utilisateur')
    app.register_blueprint(comple_compte_bp, url_prefix='/comple_compte')
    app.register_blueprint(role_bp)
    app.register_blueprint(log_in_bp, url_prefix = '/log_in')

    return app

if __name__ == '__main__':
    app = create_app()
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(e)
    app.run(debug=True, port=5000)
