
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from extension import db, decode_token
from model_db import Vendeur, Client, Utilisateur

complete_compte_bp = Blueprint("complete_compte", __name__)

def _validate_payload(payload, required):
    missing = [p for p in required if not payload.get(p)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None

@complete_compte_bp.route("/user/account/vendeur_client/complete/<string:token>", methods=["POST"])
def create_compte(token):
    # decoding the token for verification
    print(type(token))
    payload = decode_token(token)
    print(payload)
    id_utilisateur = payload.get("id_utilisateur")
    id_role = payload.get("id_role")

    # identity = get_jwt_identity()
    # if not isinstance(identity, dict):
    #     current_app.logger.error("Invalid token identity type")
    #     return jsonify({"error": {"message": "Invalid token identity"}}), 400
    #
    # id_utilisateur = identity.get("id_utilisateur")
    # id_role = identity.get("id_role")

    # checking if the is present in the database
    user = Utilisateur.query.get(id_utilisateur)
    if not user:
        return jsonify({"error": {"message": "Utilisateur introuvable"}}), 404

    # checking the id_role present in the token to perform account completion accordingly
    if user.id_role != id_role:
        return jsonify({"error": {"message": "Role mismatch"}}), 403
    data = request.get_json(silent=True) or {}
    if id_role == 2:

        # valdating the elements of the payload
        ok, err = _validate_payload(data, ["nom", "prenom", "numero", "identite"])
        if not ok:
            return jsonify({"error": {"message": err}}), 400
        new_vendeur = Vendeur(nom=data["nom"].strip(), prenom=data["prenom"].strip(),
                              numero=data["numero"].strip(), identite=data["identite"].strip(),
                              id_utilisateur=id_utilisateur)
        # adding in the database
        db.session.add(new_vendeur)

    elif id_role == 3:
        ok, err = _validate_payload(data, ["nom", "prenom", "numero"])
        if not ok:
            return jsonify({"error": {"message": err}}), 400
        new_client = Client(nom=data["nom"].strip(), prenom=data["prenom"].strip(),
                            numero=data["numero"].strip(), id_utilisateur=id_utilisateur)
        db.session.add(new_client)
    else:
        return jsonify({"error": {"message": "Role non autorisé"}}), 403
    try:
        db.session.commit()
    except IntegrityError as ie:
        db.session.rollback()
        current_app.logger.warning("IntegrityError in complete_compte: %s", ie)
        return jsonify({"error": {"message": "Conflit de données (valeurs uniques)"}}), 409
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("DB error in complete_compte")
        return jsonify({"error": {"message": "Internal server error"}}), 500
    return jsonify({"data": {"message": "Votre compte a été complété avec succès"}}), 201

