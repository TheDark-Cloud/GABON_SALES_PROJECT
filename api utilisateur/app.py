from flask import Flask
from extension import db
from routes.utilisateur import utilisateur_bp
from routes.vendeur import vendeur_bp
from routes.log_in import log_in_bp
import os
from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin@localhost:5433/api_utilisateur_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'cVUGtw10B_PRv2jaCS1IUbzxnucRIJ79fMQ4dGhUEUw'  #os.environ.get('SECRET_KEY')

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(utilisateur_bp, url_prefix='/utilisateur')
    app.register_blueprint(vendeur_bp, url_prefix='/vendeur')
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
