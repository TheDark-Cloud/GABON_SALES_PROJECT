from flask import Flask
from extension import db
from routes.utilisateur import utilisateur_bp
from routes.vendeur import vendeur_bp
from routes.log_in import log_in_bp


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin@localhost/api_utilisateur_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'change-me'

    db.init_app(app)

    app.register_blueprint(utilisateur_bp, url_prefix='/utilisateur')
    app.register_blueprint(vendeur_bp, url_prefix='/vendeur')
    app.register_blueprint(log_in_bp, url_prefix = '/log_in')
    return app

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
