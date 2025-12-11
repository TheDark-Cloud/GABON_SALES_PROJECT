from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from setting.config import db, is_valide_phone_format, validate_parameters
from setting.auth import authenticate_validator, payload_validator
from model_db import Vendeur, Client, Utilisateur
from setting.tokenize import tokenize

complete_compte_bp = Blueprint("complete_compte", __name__)
@complete_compte_bp.route("/user/account/vendeur_client/complete", methods=["POST"])
@jwt_required()
def create_compte():
    try:
        # --- Validate identity ---
        raw_identity = get_jwt_identity()
        if raw_identity is None:
            return jsonify({"error": "Invalid token: missing identity"}), 401

        try:
            identity = int(raw_identity)
        except ValueError:
            return jsonify({"error": "Invalid token: identity must be an integer"}), 401

        claims = get_jwt()
        authenticate_validator(identity, claims)

        payload = request.get_json(silent=True) or {}
        user = Utilisateur.query.filter_by(id_utilisateur=identity).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        role = claims.get("name_role")

        # --- VENDEUR ---
        if role == "vendeur":
            required_fields = ["nom", "prenom", "numero", "identite"]
            payload_validator(payload, required_fields)

            if not is_valide_phone_format(payload.get("numero")):
                return jsonify({"error": "Phone number invalide"}), 400

            if user.is_complete:
                return jsonify({"message": "Account already completed"}), 400

            if Vendeur.query.filter_by(id_utilisateur=identity).first() is not None:
                return jsonify({"error": "Vendeur already exists"}), 409

            vendeur = Vendeur(
                id_utilisateur=user.id_utilisateur,
                nom=payload.get("nom"),
                prenom=payload.get("prenom"),
                numero=payload.get("numero"),
                identite=payload.get("identite")
            )
            db.session.add(vendeur)
            user.is_complete = True
            db.session.commit()

            new_claims = {"name_role": role, "id_vendeur":vendeur.id_vendeur}
            refresh_token = tokenize(identity=str(identity), claims=new_claims)
            return jsonify({"message": "Account successfully completed", "token": refresh_token}), 200

        # --- CLIENT ---
        elif role == "client":
            required_fields = ["nom", "prenom", "numero"]
            payload_validator(payload, required_fields)

            if not is_valide_phone_format(payload.get("numero")):
                return jsonify({"error": "Phone number invalide"}), 400

            if user.is_complete:
                return jsonify({"message": "Account already completed"}), 400
            if Client.query.filter_by(id_utilisateur=identity).first() is not None:
                return jsonify({"error": "Client already exists"}), 409

            client = Client(
                id_utilisateur=user.id_utilisateur,
                nom=payload.get("nom"),
                prenom=payload.get("prenom"),
                numero=payload.get("numero"))

            db.session.add(client)
            user.is_complete = True
            db.session.commit()

            new_claims = {"is_complete": user.is_complete,"name_role": role, "id_client": client.id_client}
            refreshed_token = tokenize(identity=str(identity), claims=new_claims)
            return jsonify({"message": "Account successfully completed", "refreshed_token": refreshed_token}), 200

        # --- UNKNOWN ROLE ---
        else:
            return jsonify({"error": "Invalid role"}), 403

    except Exception as ex:
        db.session.rollback()
        db.session.close()
        return jsonify({"error": str(ex)}), 500