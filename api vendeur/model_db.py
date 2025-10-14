
from datetime import datetime, timezone
from setting.config import db

# lambda:datetime.now(timezone.utc) I is a function that automatically return the date at instance creation

class Vendeur(db.Model):
    __tablename__ = "vendeur"

    id_vendeur = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    mot_de_passe = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True) # get current time at runtime

    # table relation
    boutique = db.relationship("Boutique", backpopulates= "vendeur", uselist= False, cascade="all, delete-orphan")
    produit = db.relationship("Produit", backpopulates="vendeur", cascade="all, delete-orphan")

class Boutique(db.Model):
    __tablename__ = "boutique"

    id_boutique = db.Column(db.Integer, primary_key=True)
    id_vendeur = db.Column(db.Integer, db.ForeignKey('vendeur.id_vendeur', ondelete="CASCADE"), nullable=False)
    nom = db.Column(db.String(150), nullable=False)
    adresse = db.Column(db.Text)
    domaine = db.Column(db.String(150))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)

    # table relation
    vendeur = db.relationship("Vendeur", backpopulate="boutique", uselist=True)


class Categorie(db.Model):
    __tablename__ = "categorie"
    id_categorie = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(120), unique=True, nullable=False)

class Produit(db.Model):
    __tablename__ = "produit"
    id_produit = db.Column(db.Integer, primary_key=True)
    id_vendeur = db.Column(db.Integer, db.ForeignKey('vendeur.id_vendeur', ondelete="CASCADE"), nullable=False)
    id_categorie = db.Column(db.Integer, db.ForeignKey('categorie.id_categorie'))
    nom = db.Column(db.String(200), nullable=False)
    prix = db.Column(db.Numeric(12,2), nullable=False)
    description = db.Column(db.Text)
    quantite = db.Column(db.Integer, default=0)
    image = db.Column(db.Blo)
    est_archive = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), index=True)

    # table relation
    vendeur = db.relationship("vendeur", backpopulates="produit", uselist= True)