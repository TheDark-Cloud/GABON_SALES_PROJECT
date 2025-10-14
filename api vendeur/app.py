import os
from dotenv import load_dotenv
from flask import Flask
from setting.config import db
from flask_migrate import Migrate

db_migrate = Migrate()

def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI_API_VENDEUR')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', app.config['SECRET_KEY'])
    app.config['JWT_ALGORITHM'] = os.environ.get('JWT_ALGORITHM', "HS256")
    app.config['JWT_HEADER_TYPE'] = os.environ.get('JWT_HEADER_TYPE', "Authorization")
    app.config['JWT_HEADER_NAME'] = os.environ.get('JWT_HEADER_NAME', "Bearer")
    app.config['JWT_EXP_DELTA_SECONDS'] = int(os.environ.get('JWT_EXP_DELTA_SECONDS', "2524608000"))

    db.init_app(app)
    db_migrate.init_app(app, db)

    # registering all the routes

    return app



if __name__ == '__main__':
    try:
        app = create_app()
        with app.app_context():
            db.create_all()
            db.session.close()
    except Exception as e:
        print(e)