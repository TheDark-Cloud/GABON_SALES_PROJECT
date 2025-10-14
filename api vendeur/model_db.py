from datetime import datetime, timezone
from setting.config import db
from base64 import b64encode

# lambda:datetime.now(timezone.utc) I is a function that automatically return the date at instance creation

class Vendeur(db.Model):
    __tablename__ = "vendeur"

    id_vendeur = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    hassed_password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True) # get current time at runtime

    # table relation
    boutique = db.relationship("Boutique", back_populates= "vendeur")
    produit = db.relationship("Produit", back_populates="vendeur")

    def to_dict(self):
        return {
            "nom": self.nom,
            "email": self.email
        }

class Boutique(db.Model):
    __tablename__ = "boutique"

    id_boutique = db.Column(db.Integer, primary_key=True)
    id_vendeur = db.Column(db.Integer, db.ForeignKey('vendeur.id_vendeur', ondelete="CASCADE"), nullable=False)
    nom = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    adresse = db.Column(db.Text)
    domaine = db.Column(db.String(150))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)

    # table relation
    vendeur = db.relationship("Vendeur", back_populates="boutique")

    # methode
    def to_dict(self):
        return {
            "id_boutique": self.id_boutique,
            "id_vendeur": self.id_vendeur,
            "nom": self.nom,
            "adresse": self.adresse,
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
    produit = db.relationship("Produit", back_populates="categorie")
    # methods
    def to_dict(self):
        return {"id_categorie": self.id_categorie, "nom_categorie": self.nom_categorie}

class Produit(db.Model):
    __tablename__ = "produit"
    id_produit = db.Column(db.Integer, primary_key=True)
    id_vendeur = db.Column(db.Integer, db.ForeignKey('vendeur.id_vendeur', ondelete="CASCADE"), nullable=False)
    id_categorie = db.Column(db.Integer, db.ForeignKey('categorie.id_categorie'))
    nom = db.Column(db.String(200), nullable=False)
    prix = db.Column(db.Numeric(12,2), nullable=False)
    description = db.Column(db.Text)
    quantite = db.Column(db.Integer, default=0)
    image = db.Column(db.LargeBinary, nullable=False)
    # est_archive = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)

    # table relation
    vendeur = db.relationship("Vendeur", back_populates="produit")
    categorie = db.relationship("Categorie", back_populates="produit")

    #methode
    def to_dict(self):
        return {
            "id_categorie": self.id_categorie,
            "nom": self.nom,
            "prix": self.prix,
            "description": self.description,
            "quantite": self.quantite,
            "image": b64encode(self.image).decode("utf-8")
        }