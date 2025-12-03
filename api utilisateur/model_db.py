from setting.config import db
from datetime import datetime, timezone


def _now_utc():
    return datetime.now(timezone.utc)

class Utilisateur(db.Model):
    __tablename__ = 'utilisateur'
    id_utilisateur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mail = db.Column(db.String(200), unique=True, nullable=False)
    hashed_password = db.Column(db.String(200), nullable=False)
    is_complete = db.Column(db.Boolean())
    id_role = db.Column(db.Integer, db.ForeignKey('role.id_role'), nullable=False)
    created_at = db.Column(db.DateTime, default=_now_utc, index=True)
    phone_number = db.Column(db.String(15), nullable=False)

    role = db.relationship('Role', back_populates='utilisateur', lazy='joined')
    administrateur = db.relationship('Administrateur', back_populates='utilisateur', uselist=False, cascade="all, delete-orphan")
    vendeur = db.relationship('Vendeur', back_populates='utilisateur', uselist=False, cascade="all, delete-orphan")
    client = db.relationship('Client', back_populates='utilisateur', uselist=False, cascade="all, delete-orphan")

    def __init__(self, mail, hashed_password, phone_number, id_role, is_complete):
        self.mail = mail
        self.hashed_password = hashed_password
        self.phone_number = "+241" + phone_number
        self.id_role = id_role
        self.is_complete = False if None else is_complete

    def to_dict(self):
        return {
            'id_utilisateur': self.id_utilisateur,
            'mail': self.mail,
            # 'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Administrateur(db.Model):
    __tablename__ = 'administrateur'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=_now_utc, index=True)
    statut = db.Column(db.Boolean, default=True)

    utilisateur = db.relationship('Utilisateur', back_populates='administrateur', uselist=False)

    def __init__(self, nom, id_utilisateur=None):
        self.name = (nom or "").strip()
        if id_utilisateur is not None:
            self.id_utilisateur = id_utilisateur

    def to_dict(self):
        return {'id': self.id, 'nom': self.name, 'id_utilisateur': self.id_utilisateur}

class Vendeur(db.Model):
    __tablename__ = 'vendeur'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur', ondelete='CASCADE'), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(100), unique=True, nullable=False)
    identite = db.Column(db.String(200), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=_now_utc, index=True)
    statut = db.Column(db.Boolean, default=True)

    utilisateur = db.relationship('Utilisateur', back_populates='vendeur', uselist=False)

    def __init__(self, nom, prenom, numero, identite, id_utilisateur):
        self.nom = nom.strip()
        self.prenom = (prenom or "").strip()
        self.numero = str(numero)
        self.identite = (identite or "").strip()
        self.id_utilisateur = id_utilisateur

    def to_dict(self):
        return {"id":"vendeur_id",'id_utilisateur': self.id_utilisateur,
                'nom': self.nom, 'prenom': self.prenom,
                'numero': self.numero, 'identite': self.identite}

class Client(db.Model):
    __tablename__ = 'client'
    id_client = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur', ondelete='CASCADE'), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(100), unique=True, nullable=False)
    statut = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=_now_utc, index=True)

    utilisateur = db.relationship('Utilisateur', back_populates='client', uselist=False)

    def __init__(self, nom, prenom, numero, id_utilisateur):
        self.nom = nom.strip().ca
        self.prenom = prenom.strip()
        self.numero = str(numero)
        self.id_utilisateur = id_utilisateur

    def to_dict(self):
        return {'id_client': self.id_client,
                'nom': self.nom,
                'prenom': self.prenom,
                'numero': self.numero}


class Role(db.Model):
    __tablename__ = 'role'
    id_role = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_role = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=_now_utc, index=True)

    utilisateur = db.relationship('Utilisateur', back_populates='role', lazy=True)

    def __init__(self, name_role):
        self.name_role = name_role.strip().lower()

    def to_dict(self):
        return {'id_role': self.id_role,
                'name_role': self.name_role}