from setting.config import db
from datetime import datetime, timezone
from base64 import b64encode


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
            "id_role": self.id_role}

class Administrateur(db.Model):
    __tablename__ = 'administrateur'
    id_admin = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur', ondelete='CASCADE'), nullable=False)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=_now_utc, index=True)
    statut = db.Column(db.Boolean, default=True)

    utilisateur = db.relationship('Utilisateur', back_populates='administrateur', uselist=False)

    def __init__(self, nom, id_utilisateur=None):
        self.name = (nom or "").strip()
        if id_utilisateur is not None:
            self.id_utilisateur = id_utilisateur

    def to_dict(self):
        return {'id_admin': self.id_admin,
                'nom': self.name, 'prenom': self.prenom}

class Vendeur(db.Model):
    __tablename__ = 'vendeur'
    id_vendeur = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_utilisateur = db.Column(db.Integer, db.ForeignKey('utilisateur.id_utilisateur', ondelete='CASCADE'), nullable=False, unique=True)
    nom = db.Column(db.String(200), nullable=False)
    prenom = db.Column(db.String(200), nullable=False)
    numero = db.Column(db.String(100), unique=True, nullable=False)
    identite = db.Column(db.String(200), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=_now_utc, index=True)
    statut = db.Column(db.Boolean, default=True)

    product = db.relationship('Product', back_populates='vendeur', lazy=True)
    utilisateur = db.relationship('Utilisateur', back_populates='vendeur', uselist=False)
    boutique = db.relationship('Boutique', back_populates='vendeur', uselist=False)

    def __init__(self, nom, prenom, numero, identite, id_utilisateur):
        self.nom = nom.strip()
        self.prenom = prenom.strip()
        self.numero = "+241"+str(numero)
        self.identite = identite.strip()
        self.id_utilisateur = id_utilisateur

    def to_dict(self):
        return {"id":self.id_vendeur,
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
        self.nom = nom.strip()
        self.prenom = prenom.strip()
        self.numero = "+241"+str(numero)
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


# Temporarily added for prototyping coming from Api-Vendeur

class Product(db.Model):
    __tablename__ = "product"
    id_product = db.Column(db.Integer, primary_key=True)
    id_vendeur = db.Column(db.Integer, db.ForeignKey('vendeur.id_vendeur', ondelete="CASCADE"), nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('categorie.id_categorie'))
    product_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Numeric(12, 2), nullable=False)
    description = db.Column(db.Text)
    quantity = db.Column(db.Integer, default=0)
    image = db.Column(db.LargeBinary, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # table relation
    vendeur = db.relationship("Vendeur", back_populates="product")
    categorie = db.relationship("Categorie", back_populates="product")

    # methode
    def __init__(self, id_vendeur, product_name, price, description, quantity, image):
        self.id_vendeur = id_vendeur
        self.product_name = product_name
        self.price = price
        self.description = description
        self.quantity = quantity
        self.image = image

    def to_dict(self):
        return {"id_product": self.id_product,
                "categorie": self.categorie.nom_categorie,
                "product_name": self.product_name,
                "price": self.price,
                "description": self.description,
                "quantity": self.quantity,
                "image": b64encode(self.image).decode("utf-8")}



class Boutique(db.Model):
    __tablename__ = "boutique"

    id_boutique = db.Column(db.Integer, primary_key=True)
    id_vendeur = db.Column(db.Integer, db.ForeignKey('vendeur.id_vendeur', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=True)
    domaine = db.Column(db.String(150) ,nullable=True ,unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    # table relation
    vendeur = db.relationship("Vendeur", back_populates="boutique")

    def __init__(self, id_vendeur, name, email, address, domaine, description):
        self.id_vendeur = id_vendeur
        self.name = name
        self.email = email
        self.address = address
        self.domaine = domaine
        self.description = description
    # methode
    def to_dict(self):
        return {
            "id_boutique": self.id_boutique,
            "id_vendeur": self.id_vendeur,
            "name": self.name,
            "address": self.address,
            "domaine": self.domaine,
            "description": self.description,
            "created_at": self.created_at
        }

class Categorie(db.Model):
    __tablename__ = "categorie"
    id_categorie = db.Column(db.Integer, primary_key=True)
    nom_categorie= db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, nom_categorie):
        self.nom_categorie = nom_categorie

    # relations
    product = db.relationship("Product", back_populates="categorie")
    # methods
    def to_dict(self):
        return {"id_categorie": self.id_categorie,
                "nom_categorie": self.nom_categorie}