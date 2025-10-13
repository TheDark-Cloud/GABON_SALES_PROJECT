# from flask import Blueprint, request, jsonify, current_app
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# from extension import db, decode_token
# from model_db import Vendeur, Client, Utilisateur
#
# complete_compte_bp = Blueprint("complete_compte", __name__)
#
# def _validate_payload(payload, required):
#     missing = [p for p in required if not payload.get(p)]
#     if missing:
#         return False, f"Missing required fields: {', '.join(missing)}"
#     return True, None
#
# @complete_compte_bp.route("/user/account/vendeur_client/complete/<string:token>", methods=["POST"])
# def create_compte(token):
#     # decoding the token for verification
#     print(type(token))
#     payload = decode_token(token)
#     print(payload)
#     id_utilisateur = payload.get("id_utilisateur")
#     id_role = payload.get("id_role")
#
#     # identity = get_jwt_identity()
#     # if not isinstance(identity, dict):
#     #     current_app.logger.error("Invalid token identity type")
#     #     return jsonify({"error": {"message": "Invalid token identity"}}), 400
#     #
#     # id_utilisateur = identity.get("id_utilisateur")
#     # id_role = identity.get("id_role")
#
#     # checking if the is present in the database
#     user = Utilisateur.query.get(id_utilisateur)
#     if not user:
#         return jsonify({"error": {"message": "Utilisateur introuvable"}}), 404
#
#     # checking the id_role present in the token to perform account completion accordingly
#     if user.id_role != id_role:
#         return jsonify({"error": {"message": "Role mismatch"}}), 403
#     data = request.get_json(silent=True) or {}
#     if id_role == 2:
#
#         # valdating the elements of the payload
#         ok, err = _validate_payload(data, ["nom", "prenom", "numero", "identite"])
#         if not ok:
#             return jsonify({"error": {"message": err}}), 400
#         new_vendeur = Vendeur(nom=data["nom"].strip(), prenom=data["prenom"].strip(),
#                               numero=data["numero"].strip(), identite=data["identite"].strip(),
#                               id_utilisateur=id_utilisateur)
#         # adding in the database
#         db.session.add(new_vendeur)
#
#     elif id_role == 3:
#         ok, err = _validate_payload(data, ["nom", "prenom", "numero"])
#         if not ok:
#             return jsonify({"error": {"message": err}}), 400
#         new_client = Client(nom=data["nom"].strip(), prenom=data["prenom"].strip(),
#                             numero=data["numero"].strip(), id_utilisateur=id_utilisateur)
#         db.session.add(new_client)
#     else:
#         return jsonify({"error": {"message": "Role non autorisé"}}), 403
#     try:
#         db.session.commit()
#     except IntegrityError as ie:
#         db.session.rollback()
#         current_app.logger.warning("IntegrityError in complete_compte: %s", ie)
#         return jsonify({"error": {"message": "Conflit de données (valeurs uniques)"}}), 409
#     except SQLAlchemyError:
#         db.session.rollback()
#         current_app.logger.exception("DB error in complete_compte")
#         return jsonify({"error": {"message": "Internal server error"}}), 500
#     return jsonify({"data": {"message": "Votre compte a été complété avec succès"}}), 201
#
# ------------------------------------------------------------------------------------------------------------------------

# from flask import Blueprint, request, jsonify, current_app
# from sqlalchemy.exc import IntegrityError, SQLAlchemyError
# from extension import db, decode_token
# from model_db import Vendeur, Client, Utilisateur
#
# complete_compte_bp = Blueprint("complete_compte", __name__)
#
# def _validate_payload(payload, required):
#     missing = [p for p in required if not payload.get(p)]
#     if missing:
#         return False, f"Missing required fields: {', '.join(missing)}"
#     return True, None
#
# @complete_compte_bp.route("/user/account/vendeur_client/complete/<string:token>", methods=["POST"])
# def create_compte(token):
#     try:
#         payload = decode_token(token)
#     except Exception:
#         current_app.logger.exception("Token decode failed")
#         return jsonify({"error": {"message": "Invalid or expired token"}}), 400
#
#     if not isinstance(payload, dict):
#         current_app.logger.error("Decoded token payload is not a dict")
#         return jsonify({"error": {"message": "Invalid token payload"}}), 400
#
#     id_utilisateur = payload.get("id_utilisateur")
#     id_role = payload.get("id_role")
#     if id_utilisateur is None or id_role is None:
#         return jsonify({"error": {"message": "Token missing identity fields"}}), 400
#
#     user = Utilisateur.query.get(id_utilisateur)
#     if not user:
#         return jsonify({"error": {"message": "Utilisateur introuvable"}}), 404
#
#     if user.id_role != id_role:
#         return jsonify({"error": {"message": "Role mismatch"}}), 403
#
#     data = request.get_json(silent=True) or {}
#
#     # Prevent completing twice
#     if id_role == 2:
#         if user.vendeur is not None:
#             return jsonify({"error": {"message": "Compte vendeur déjà complété"}}), 409
#         ok, err = _validate_payload(data, ["nom", "prenom", "numero", "identite"])
#         if not ok:
#             return jsonify({"error": {"message": err}}), 400
#         try:
#             new_vendeur = Vendeur(
#                 nom=data["nom"].strip(),
#                 prenom=data["prenom"].strip(),
#                 numero=data["numero"].strip(),
#                 identite=data["identite"].strip(),
#                 id_utilisateur=id_utilisateur
#             )
#             db.session.add(new_vendeur)
#         except ValueError as ve:
#             return jsonify({"error": {"message": str(ve)}}), 400
#
#     elif id_role == 3:
#         if user.client is not None:
#             return jsonify({"error": {"message": "Compte client déjà complété"}}), 409
#         ok, err = _validate_payload(data, ["nom", "prenom", "numero"])
#         if not ok:
#             return jsonify({"error": {"message": err}}), 400
#         try:
#             new_client = Client(
#                 nom=data["nom"].strip(),
#                 prenom=data["prenom"].strip(),
#                 numero=data["numero"].strip(),
#                 id_utilisateur=id_utilisateur
#             )
#             db.session.add(new_client)
#         except ValueError as ve:
#             return jsonify({"error": {"message": str(ve)}}), 400
#
#     else:
#         return jsonify({"error": {"message": "Role non autorisé"}}), 403
#
#     try:
#         db.session.commit()
#     except IntegrityError as ie:
#         db.session.rollback()
#         current_app.logger.warning("IntegrityError in complete_compte: %s", ie)
#         return jsonify({"error": {"message": "Conflit de données (valeurs uniques)"}}), 409
#     except SQLAlchemyError:
#         db.session.rollback()
#         current_app.logger.exception("DB error in complete_compte")
#         return jsonify({"error": {"message": "Internal server error"}}), 500
#
#     return jsonify({"data": {"message": "Votre compte a été complété avec succès"}}), 201
# ----------------------------------------------------------------------------------------------------------------------
# routes/complete_compte.py
from flask import Blueprint, request, jsonify, current_app
from functools import wraps
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from extension import db, decode_token
from model_db import Vendeur, Client, Utilisateur

complete_compte_bp = Blueprint("complete_compte", __name__)

def _validate_payload(payload, required):
    missing = [p for p in required if not payload.get(p)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None

def _extract_bearer_token():
    auth = request.headers.get("Authorization", "")
    if not auth:
        return None, (jsonify({"error": {"message": "Missing Authorization header"}}), 401)
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None, (jsonify({"error": {"message": "Invalid Authorization header format"}}), 401)
    return parts[1], None

def require_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token, err = _extract_bearer_token()
        if err:
            return err
        try:
            payload = decode_token(token)
        except ValueError as e:
            current_app.logger.info("Token decode error: %s", e)
            return jsonify({"error": {"message": str(e)}}), 401
        if not isinstance(payload, dict):
            return jsonify({"error": {"message": "Invalid token payload"}}), 401
        kwargs["_token_payload"] = payload
        return fn(*args, **kwargs)
    return wrapper

@complete_compte_bp.route("/user/account/vendeur_client/complete", methods=["POST"])
@require_token
def create_compte(_token_payload=None):
    """
    Complete a Vendeur or Client account.
    Token payload must include id_utilisateur and id_role.
    Token must be sent in Authorization header as Bearer <token>.
    """
    payload = _token_payload
    id_utilisateur = payload.get("id_utilisateur")
    id_role = payload.get("id_role")
    if id_utilisateur is None or id_role is None:
        return jsonify({"error": {"message": "Token missing identity fields"}}), 400

    user = Utilisateur.query.get(id_utilisateur)
    if not user:
        return jsonify({"error": {"message": "Utilisateur introuvable"}}), 404

    if user.id_role != id_role:
        return jsonify({"error": {"message": "Role mismatch"}}), 403

    data = request.get_json(silent=True) or {}

    if id_role == 2:
        if user.vendeur is not None:
            return jsonify({"error": {"message": "Compte vendeur déjà complété"}}), 409
        ok, err = _validate_payload(data, ["nom", "prenom", "numero", "identite"])
        if not ok:
            return jsonify({"error": {"message": err}}), 400
        try:
            new_vendeur = Vendeur(
                nom=data["nom"].strip(),
                prenom=data["prenom"].strip(),
                numero=data["numero"].strip(),
                identite=data["identite"].strip(),
                id_utilisateur=id_utilisateur
            )
            db.session.add(new_vendeur)
        except ValueError as ve:
            return jsonify({"error": {"message": str(ve)}}), 400

    elif id_role == 3:
        if user.client is not None:
            return jsonify({"error": {"message": "Compte client déjà complété"}}), 409
        ok, err = _validate_payload(data, ["nom", "prenom", "numero"])
        if not ok:
            return jsonify({"error": {"message": err}}), 400
        try:
            new_client = Client(
                nom=data["nom"].strip(),
                prenom=data["prenom"].strip(),
                numero=data["numero"].strip(),
                id_utilisateur=id_utilisateur
            )
            db.session.add(new_client)
        except ValueError as ve:
            return jsonify({"error": {"message": str(ve)}}), 400

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