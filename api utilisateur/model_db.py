from extension import db
from datetime import datetime, timezone
import re

# class SerializerMixin:
#     __abstract__ = True
#     def __init__(self):
#         self.__table__ = None
#
#     def to_dict(self):
#         result = {}
#         for column in self.__table__.columns:
#             column_name = column.name
#             column_value = getattr(self, column_name)
#
#             # Handle datetime formatting
#             if hasattr(column.type, 'python_type') and column.type.python_type.__name__ == 'datetime':
#                 if column_value:
#                     result[column_name] = column_value.isoformat()
#                 else:
#                     result[column_name] = None
#             else:
#                 result[column_name] = column_value
#
#         return result

class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    id_role = db.Column(db.Integer, db.ForeignKey('role.id_role'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)

    administrateur = db.relationship('Administrateur', backref='utilisateur', uselist=False)
    vendeur = db.relationship('Vendeur', backref='utilisateur', uselist=False)
    client = db.relationship('Client', backref='utilisateur', uselist=False)

    def __init__(self, email, password, id_role):
        super().__init__()
        pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        if not re.match(pattern, email):
            raise ValueError('Format du mail invalide!')
        if len(password) < 8:
            raise ValueError('Mot de passe doit être composé de 8 caractères!')
        self.email = email.strip().lower()
        self.password = password
        self.id_role = id_role



class Administrateur(db.Model):
    __tablename__ = 'administrateur'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)
    statut = db.Column(db.Boolean, default=True)

    def __init__(self, nom):
        super().__init__()
        self.nom = nom


class Vendeur(db.Model):
    __tablename__ = 'vendeur'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)
    statut = db.Column(db.Boolean, default=True)

    def __init__(self, nom, prenom, numero):
        super().__init__()
        self.nom = nom
        self.prenom = prenom
        check_numero(numero)
        self.numero = numero


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(100), nullable=False)
    statut = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_role = db.Column(db.String(100), nullable=False)

    utilisateurs = db.relationship('Utilisateur', backref='role', lazy=True)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)


# verification du numero
def check_numero(numero):
    for _ in range(len(numero)):
        if numero[_].isdigit():
            return numero
        else:
            raise ValueError('Le numero ne doit comporter que des chifres!')
