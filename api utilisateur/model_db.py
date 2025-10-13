from extension import db
from datetime import datetime, timezone
import re
from werkzeug.security import generate_password_hash, check_password_hash

EMAIL_REGEX = re.compile(r'^[A-Za-z0-9_.+-]+@[A-Za-z0-9-]+\.[A-Za-z0-9-.]+$')
PHONE_REGEX = re.compile(r'^\d{7,15}$')

class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    id_utilisateur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    id_role = db.Column(db.Integer, db.ForeignKey('role.id_role'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    role = db.relationship('Role', back_populates='utilisateur', lazy='joined')
    administrateur = db.relationship('Administrateur', back_populates='utilisateur', uselist=False, cascade="all, delete-orphan")
    vendeur = db.relationship('Vendeur', back_populates='utilisateur', uselist=False, cascade="all, delete-orphan")
    client = db.relationship('Client', back_populates='utilisateur', uselist=False, cascade="all, delete-orphan")

    def __init__(self, email, password, id_role):
        email = (email or "").strip().lower()
        if not EMAIL_REGEX.fullmatch(email):
            raise ValueError("Format du mail invalide")
        if not password or len(password) < 8:
            raise ValueError("Mot de passe doit être composé de 8 caractères minimum")
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.id_role = id_role

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id_utilisateur': self.id_utilisateur,
            'email': self.email,
            'id_role': self.id_role,
        }

class Administrateur(db.Model):
    __tablename__ = 'administrateur'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur', ondelete='CASCADE'), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    statut = db.Column(db.Boolean, default=True)

    utilisateur = db.relationship('Utilisateur', back_populates='administrateur', uselist=False)

    def __init__(self, nom):
        self.nom = (nom or "").strip()

    def to_dict(self):
        return {'id': self.id, 'nom': self.nom}

class Vendeur(db.Model):
    __tablename__ = 'vendeur'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur', ondelete='CASCADE'), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(100), unique=True, nullable=False)
    identite = db.Column(db.String(200), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    statut = db.Column(db.Boolean, default=True)

    utilisateur = db.relationship('Utilisateur', back_populates='vendeur', uselist=False)

    def __init__(self, nom, prenom, numero, identite, id_utilisateur):
        if not PHONE_REGEX.fullmatch(numero):
            raise ValueError("Le numero doit contenir uniquement des chiffres et longueur valide")
        self.nom = (nom or "").strip()
        self.prenom = (prenom or "").strip()
        self.numero = numero
        self.identite = (identite or "").strip()
        self.id_utilisateur = id_utilisateur

    def to_dict(self):
        return {'id': self.id, 'nom': self.nom, 'prenom': self.prenom, 'numero': self.numero}

class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur', ondelete='CASCADE'), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(100), unique=True, nullable=False)
    statut = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    utilisateur = db.relationship('Utilisateur', back_populates='client', uselist=False)

    def __init__(self, nom, prenom, numero, id_utilisateur):
        if not PHONE_REGEX.fullmatch(numero):
            raise ValueError("Le numero doit contenir uniquement des chiffres et longueur valide")
        self.nom = (nom or "").strip()
        self.prenom = (prenom or "").strip()
        self.numero = numero
        self.id_utilisateur = id_utilisateur

    def to_dict(self):
        return {'id': self.id, 'nom': self.nom, 'prenom': self.prenom, 'numero': self.numero}

class Role(db.Model):
    __tablename__ = 'role'
    id_role = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_role = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    utilisateur = db.relationship('Utilisateur', back_populates='role', lazy=True)

    def __init__(self, id_role, nom_role):
        self.id_role = id_role
        self.nom_role = nom_role
    def to_dict(self):
        return {'id': self.id_role, 'nom_role': self.nom_role}