from flask import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

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


class Produit(db.Model, SerializerMixin):
    __tablename__ = 'produit'

    id_vendeur = db.Column(db.Interger, primary_key=True)
    nom_produit = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    quantite = db.Column(db.Integer, nullable=False, default=0)
    image = db.Column(db.BLOB, nullable=False)
    categorie = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Boutique(db.Model, SerializerMixin):
    __tablename__ = 'boutique'

    nom_boutique = db.Column(db.String, nullable=False)
    adresse_boutique = db.column(db.String(200), nullable=False)
    type_de_boutique = db.column(db.String(200), nullable=True)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
