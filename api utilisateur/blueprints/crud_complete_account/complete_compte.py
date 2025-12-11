from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from setting.config import db, is_valide_phone_format
from setting.auth import authenticate_validator, payload_validator
from model_db import Vendeur, Client, Utilisateur

complete_compte_bp = Blueprint("complete_compte", __name__)


@complete_compte_bp.route("/user/account/vendeur_client/complete", methods=["POST"])
@jwt_required
def create_compte(_token_payload=None):

    """ COMPLETE THE ACCOUNT"""
    try:
        identity = get_jwt_identity()
        claims = get_jwt()
        authenticate_validator(identity, claims)

        payload = request.get_json(silent=True) or {}
        user = Utilisateur.query.get_or_404(identity["id_utilisateur"]).first()

        if claims.get('name_role') != 'vendeur':
            required_fields = ["nom", "prenom", "numero", "identite"]
            payload_validator(payload, required_fields)
            if not is_valide_phone_format(payload.get("numero")):
                return jsonify({"error": "Phone number invalide"}), 400

            if user.is_complete:
                return jsonify({"message": "Account already completed"}), 400
            admin = Vendeur(id_utilisateur=user.id_utilisateur,
                            nom=payload.get("nom"),
                            prenom=payload.get('prenom'),
                            numero=payload.get('numero'),
                            identite=payload.get('identite'))
            db.session.add(admin)
            user.is_complete = True
            db.session.commit()
            return jsonify({"message": "Account successfully completed"}), 200

        if claims.get('name_role') != 'client':
            required_fields = ["nom", "prenom", "numero"]
            payload_validator(payload, required_fields)
            if not is_valide_phone_format(payload.get("numero")):
                return jsonify({"error": "Phone number invalide"}), 400

            if not user.is_complete:
                return jsonify({"message": "Account already completed"}), 400

            client = Client(id_utilisateur=user.id_utilisateur,
                            nom=payload.get("nom"),
                            prenom=payload.get('prenom'),
                            numero=payload.get('numero'))
            db.session.add(client)
            user.is_complete = True
            db.session.commit()
            return jsonify({"message": "Account successfully completed"}), 200

    except Exception as ex:
        return jsonify({"error": str(ex)}), 500