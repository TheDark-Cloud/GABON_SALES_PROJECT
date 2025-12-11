from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from model_db import Boutique, Utilisateur, Vendeur
from setting.config import db
from setting.auth import authenticate_validator, payload_validator

add_shop_bp = Blueprint('add_shop', __name__)

@add_shop_bp.route('/vendeur/add_shop', methods=['POST'])
@jwt_required()
def add_shop():
    print("Adding shop")
    """
    Add a shop in the database
    expected data
    identity: id_vendeur = user.id_utilisateur
    claims: {"id_vendeur: user.vendeur.id_vendeur, "name_role": "vendeur"}

    """

    claims = get_jwt()
    identity = int(get_jwt_identity())

    authenticate_validator(identity=identity, claims=claims)

    payload = request.get_json()
    required_fields = ['name', 'address', 'domaine', 'description']

    payload_validator(payload, required_fields)
    user = Utilisateur.query.filter_by(id_utilisateur=identity).first()
    vendeur = Vendeur.query.filter_by(id_vendeur=claims.get('id_vendeur')).first()
    boutique = Boutique.query.filter_by(id_vendeur=claims.get('id_vendeur')).first()
    if user is None:
        return jsonify({"error": "user not found"}), 404
    if boutique:
        return jsonify({"error": "A shop is already registered to this vendor"}), 409
    if claims.get('id_vendeur') is None:
        return jsonify({"error": "Unauthorized access"}), 403

    if claims.get('name_role') != 'vendeur':
        return jsonify({"error": "Unauthorized role"}), 403
    try:
        shop = Boutique(id_vendeur=vendeur.id_vendeur,
                        name=payload.get('name'),
                        email=user.mail,
                        address=payload.get('address'),
                        domaine=payload.get('domaine'),
                        description=payload.get('description'))
        db.session.add(shop)
        db.session.commit()
        return jsonify({"message": "Shop added successfully",
                        "shop_data": shop.to_dict()}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500