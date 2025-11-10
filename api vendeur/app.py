import os
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager

from blueprints.crud_categorie.add_category import add_categorie_bp
from blueprints.crud_categorie.get_category import get_categorie_bp
from blueprints.crud_produit.add_product import add_product_bp
from blueprints.crud_produit.delete_product import delete_product_bp
from blueprints.crud_produit.update_product import update_product_bp

from setting.config import db
from flask_migrate import Migrate

db_migrate = Migrate()

def create_app():
    load_dotenv()
    myapp = Flask(__name__)

    myapp.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    myapp.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI_API_VENDEUR')
    myapp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    myapp.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', myapp.config['SECRET_KEY'])
    myapp.config['JWT_ALGORITHM'] = os.environ.get('JWT_ALGORITHM', "HS256")
    myapp.config['JWT_HEADER_TYPE'] = os.environ.get('JWT_HEADER_TYPE', "Authorization")
    myapp.config['JWT_HEADER_NAME'] = os.environ.get('JWT_HEADER_NAME', "Bearer")
    myapp.config['JWT_EXP_DELTA_SECONDS'] = int(os.environ.get('JWT_EXP_DELTA_SECONDS', "2524608000"))

    jwt_manager = JWTManager(myapp)

    db.init_app(myapp)
    db_migrate.init_app(myapp, db)

    # registering all the route
    # Category
    myapp.register_blueprint(get_categorie_bp)
    myapp.register_blueprint(add_categorie_bp)

    # Product
    myapp.register_blueprint(add_product_bp)
    myapp.register_blueprint(delete_product_bp)
    myapp.register_blueprint(update_product_bp)

    return myapp



if __name__ == '__main__':
    app = create_app()
    try:
        with app.app_context():
            db.create_all()

    except Exception as e:
        print(e)

    app.run(debug=True, port=5000)