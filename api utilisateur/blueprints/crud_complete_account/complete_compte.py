from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from setting.config import db
from setting.auth import authenticate_validator, payload_validator
from model_db import Vendor, Client, Utilisateur

complete_compte_bp = Blueprint("complete_compte", __name__)


@complete_compte_bp.route("/user/account/vendeur_client/complete", methods=["POST"])
@jwt_required
def create_compte(_token_payload=None):

    """ COMPLETE THE ACCOUNT"""
    identity = get_jwt_identity()
    claims = get_jwt()




    # --- Validate token identity fields ---
    payload = _token_payload or {}
    id_utilisateur = payload.get("id_utilisateur")
    id_role = payload.get("id_role")
    if id_utilisateur is None or id_role is None:
        return jsonify({"error": {"message": "Token missing identity fields"}}), 400

    # --- Load the base Utilisateur record and confirm role consistency ---
    user = Utilisateur.query.get(id_utilisateur)
    if not user:
        return jsonify({"error": {"message": "Utilisateur introuvable"}}), 404
    if user.id_role != id_role:
        # Prevent a token for one role from completing an account for another role
        return jsonify({"error": {"message": "Role mismatch"}}), 403

    # --- Parse JSON body safely; use empty dict if missing to yield useful validation errors ---
    data = request.get_json(silent=True) or {}

    # --- Vendeur completion flow (role == 2) ---
    if int(id_role) == 2:
        # Prevent duplicate completion if a related Vendeur already exists
        if getattr(user, "vendeur", None) is not None:
            return jsonify({"error": {"message": "Compte vendeur déjà complété"}}), 409

        # Validate required fields for vendor; identite required for vendeur
        ok, err = _validate_payload(data, ["nom", "prenom", "numero", "identite"])
        if not ok:
            return jsonify({"error": {"message": err}}), 400

        # Create Vendeur instance and add to session
        try:
            new_vendeur = Vendor(
                nom=data["nom"].strip(),
                prenom=data["prenom"].strip(),
                numero=data["numero"].strip(),
                identite=data["identite"].strip(),
                id_utilisateur=id_utilisateur
            )
            db.session.add(new_vendeur)
        except ValueError as ve:
            # Model-level validation raising ValueError (if any)
            return jsonify({"error": {"message": str(ve)}}), 400

    # --- Client completion flow (role == 3) ---
    elif int(id_role) == 3:
        # Prevent duplicate completion if a related Client already exists
        if getattr(user, "client", None) is not None:
            return jsonify({"error": {"message": "Compte client déjà complété"}}), 409

        # Validate required fields for client (no identite required)
        ok, err = _validate_payload(data, ["nom", "prenom", "numero"])
        if not ok:
            return jsonify({"error": {"message": err}}), 400

        # Create Client instance and add to session
        try:
            new_client = Client(
                nom=data["nom"].strip(),
                prenom=data["prenom"].strip(),
                numero=data["numero"].strip(),
                id_utilisateur=id_utilisateur
            )
            db.session.add(new_client)
        except ValueError as ve:
            # Model-level validation raising ValueError (if any)
            return jsonify({"error": {"message": str(ve)}}), 400

    # --- Unsupported roles ---
    else:
        return jsonify({"error": {"message": "Role non autorisé"}}), 403

    # --- Commit transaction with robust error handling ---
    try:
        db.session.commit()
    except IntegrityError as ie:
        # Unique constraint or other integrity problems; rollback and return conflict
        db.session.rollback()
        current_app.logger.warning("IntegrityError in complete_compte: %s", ie)
        return jsonify({"error": {"message": "Conflit de données (valeurs uniques)"}}), 409
    except SQLAlchemyError:
        # Generic DB error; rollback and return 500
        db.session.rollback()
        current_app.logger.exception("DB error in complete_compte")
        return jsonify({"error": {"message": "Internal server error"}}), 500

    # --- Success response ---
    return jsonify({"data": {"message": "Votre compte a été complété avec succès"}}), 201