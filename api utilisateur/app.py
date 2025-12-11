import os
from flask import Flask
from model_db import Role
from setting.config import db
from blueprints.crud_utilisateur.create_user import create_user_bp
from blueprints.crud_utilisateur.delete_user import delete_user_bp
from blueprints.crud_utilisateur.get_user import get_user_bp
from blueprints.crud_utilisateur.update_user import update_user_bp
from blueprints.crud_complete_account.complete_compte import complete_compte_bp
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv


migrate = Migrate()

load_dotenv()
def create_app():
    my_app = Flask(__name__)
    my_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI_API_UTILISATEUR')
    my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    my_app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    my_app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    my_app.config["JWT_ALGORITHM"] = os.environ.get('JWT_ALGORITHM')
    my_app.config["JWT_ALGORITHM_HPW"] = os.environ.get('JWT_ALGORITHM_HPW')
    my_app.config['JWT_EXP_DELTA_SECONDS'] = int(os.environ.get('JWT_EXP_DELTA_SECONDS'))


    db.init_app(my_app)
    jwt = JWTManager(my_app)
    migrate.init_app(my_app, db)

    # route user
    my_app.register_blueprint(create_user_bp)
    my_app.register_blueprint(delete_user_bp)
    my_app.register_blueprint(get_user_bp)
    my_app.register_blueprint(update_user_bp)

    # Complete compte
    my_app.register_blueprint(complete_compte_bp)


    return my_app

if __name__ == '__main__':
    app = create_app()
    try:
        with app.app_context():
            db.create_all()
            # db.session.add(Role(name_role="admin"))
            # db.session.add(Role(name_role="vendeur"))
            # db.session.add(Role(name_role="client"))
            db.session.commit()
    except Exception as e:
        print(e)

    app.run(debug=True, port=5000)

