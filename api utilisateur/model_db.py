from idlelib.configdialog import is_int

from flask import SQLAlchemy
from extension import db
from datetime import datetime
import re

'''
Table :  
Utilisateur (email, mot de passe, id rôle),  
Administrateur (id, id utilisateur, nom, prénom, numéro),  
Vendeur (id, id utilisateur, nom, prénom, pièce d’identité, numéro),  
Client (id, id utilisateur, nom prénom, numéro),  
Rôle ou catégorie du compte (id, nom rôle) 
'''


class SerializerMixin:
    def __init__(self):
        self.__table__ = None

    def to_dict(self):
        result = {}
        for column in self.__table__.columns:
            column_name = column.name
            column_value = getattr(self, column_name)

            # Handle datetime formatting
            if hasattr(column.type, 'python_type') and column.type.python_type.__name__ == 'datetime':
                if column_value:
                    result[column_name] = column_value.isoformat()
                else:
                    result[column_name] = None
            else:
                result[column_name] = column_value

        return result

class Utilisateur(db.Model, SerializerMixin):
    __tablename__ = 'utilisateur'

    id_utilisateur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_role = db.Column(db.Integer, db.Foreignkey('role.id'))
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, email, password, id_role):
        super().__init__()

        pattern = re.compile('^[a-zA-Z0-9_.-] + @[a-zA-Z0-9_.-]\.[a-zA-Z0-9_.-]+$')
        if not re.match(pattern, email):
            raise ValueError('Format du mail invalide!')

        if len(password) < 8:
            raise ValueError('Mot de passe doit etre compose de 8 caracteres!')

        self.email = email.strip().lower()
        self.password = password
        self.id_role = id_role



class Administrateur(db.Model, SerializerMixin, Utilisateur):
    __tablename__ = 'administrateur'

    id_administrateur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_role'))
    nom = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.Boolean, defaut=True)

    def __init__(self, nom):
        super().__init__()
        self.nom = nom

class Vendeur(db.Model, SerializerMixin, Utilisateur):
    _tablename__ = 'vendeur'

    id_vendeur = db.column(db.Integer, primary_key=True, autoincrement=True)
    id_utilissateur = db.column(db.Integer, db.Foreignkey('utilisateur.id_role'))
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.Boolean, defaut=True)

    def __init__(self, nom, prenom, numero):
        super().__init__()

        self.nom = nom
        self.prenom = prenom
        check_numero(self.numero)



class Client(db.Model, SerializerMixin, Utilisateur):
    __tablename__ = 'client'

    id_client = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String, nullable=False)
    statut = db.Column(db.Boolean, defaut=True)


class Role(db.Model, SerializerMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_role = db.Column(db.String(200), nullable=False)

# verification du numero
def check_numero(numero):
    for _ in range(len(numero)):
        if is_alph(_):
            numero = numero
    else:
        raise ValueError('Format du numero invalide!')