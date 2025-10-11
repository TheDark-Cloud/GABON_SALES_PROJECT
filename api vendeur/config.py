from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
migrate = Migrate()
db = SQLAlchemy()

def create_app(app):

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin@localhost:5432/api_vendeur_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'super-secret'

    app.register_blueprint(boutique_bp, url_prefix='/boutique')
    app.register_blueprint(produit_bp, url_prefix='/produit')


    db.init_app(app)
    migrate.init_app(app, db)
    return app

def create_tables(app):
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        print(e)
