from extension import db
from datetime import datetime, timezone
import re


class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'

    id_utilisateur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    id_role = db.Column(db.Integer, db.ForeignKey('role.id_role'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)

    # Relation
    role = db.relationship('Role', back_populates='utilisateur', lazy='joined')
    administrateur = db.relationship('Administrateur', back_populates='utilisateur', uselist=False)
    vendeur = db.relationship('Vendeur', back_populates='utilisateur', uselist=False)
    client = db.relationship('Client', back_populates='utilisateur', uselist=False)

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

    def to_dict(self):
        return {
            'id':self.id_utilisateur,
            'email':self.email,
            'password':self.password,
            'id_role':self.id_role
        }


class Administrateur(db.Model):
    __tablename__ = 'administrateur'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)
    statut = db.Column(db.Boolean, default=True)

    def __init__(self, nom):
        super().__init__()
        self.nom = nom

    utilisateur = db.relationship('Utilisateur', back_populates='administrateur', uselist=False)

    def to_dict(self):
        return {
            'id':self.id,
            'nom':self.nom
        }

class Vendeur(db.Model):
    __tablename__ = 'vendeur'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(100), unique=True, nullable=False)
    identite = db.Column(db.String(200), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)
    statut = db.Column(db.Boolean, default=True)

    def __init__(self, nom, prenom, numero, identite, id_utilisateur):
        super().__init__()
        self.nom = nom
        self.prenom = prenom
        check_numero(numero)
        self.numero = numero
        self.identite = identite
        self.id_utilisateur = id_utilisateur

    utilisateur = db.relationship('Utilisateur', back_populates='vendeur', uselist=False)


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur'), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(100), unique=True, nullable=False)
    statut = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)

    def __init__(self, nom, prenom, numero, id_utilisateur):
        super().__init__()
        self.nom = nom
        self.prenom = prenom
        check_numero(numero)
        self.numero = numero
        self.id_utilisateur = id_utilisateur

    utilisateur = db.relationship('Utilisateur', back_populates='client', uselist=False)

    def to_dict(self):
        return

class Role(db.Model):
    __tablename__ = 'role'

    id_role= db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_role = db.Column(db.String(100), unique=True, nullable=False)

    utilisateur = db.relationship('Utilisateur', back_populates='role', lazy=True)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)
    def to_dict(self):
        return {
            'id':self.id_role,
            'nom_role':self.nom_role,
        }

# verification du numero
def check_numero(numero):
    for _ in range(len(numero)):
        if numero[_].isdigit():
            return numero
        else:
            raise ValueError('Le numero ne doit comporter que des chifres!')
