from flask import Response, Blueprint, request, current_app, jsonify, session
from apps.usuarios.models import Users
from apps.usuarios.schemas.users import UserSchema
from apps.usuarios.users_utils.validate.password_hash import pass_hash
from apps.usuarios.users_utils.validate.validate_user import validate_user
from apps.usuarios.users_utils.jwt.access import generate_token
from apps.usuarios.users_utils.jwt.validate import jwt_required
from apps.usuarios.users_utils.jwt.refresh import refresh
from apps.usuarios.users_utils.validate.permissions import is_admin
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route("/login/", methods=["POST"])
def login():
    try:
        db_session = current_app.config["SESSION"]()
        username = request.json.get("email")
        password = request.json.get("password")
        valid_user = validate_user(username, password)
        if valid_user:
            session["user_id"] = valid_user.id
            token = generate_token(valid_user)
            return jsonify(token), 200
    except Exception as e:
        return jsonify({"error:": str(e)}), 200


@user_blueprint.route("/users/refresh_token/", methods=["POST"])
def refresh_token():
    try:
        token = request.json.get("refresh_token")
        new_token = refresh(token)
        return jsonify(new_token), 200
    except Exception as e:
        return jsonify({"error:": str(e)}), 200


@user_blueprint.route("/users/register/", methods=["POST"])
@jwt_required
@is_admin
def register_user():
    db_session = current_app.config["SESSION"]()
    json_input = request.get_json()
    try:
        users_schema = UserSchema()
        data = users_schema.load(json_input)
        data["password"] = pass_hash(data["password"])
        user = Users(**data)
        db_session.add(user)
        db_session.commit()
    except ValidationError as e:
        return Response(e.messages, status=500)
    except SQLAlchemyError as e:
        return Response("Error", status=500)
    finally:
        db_session.close()
    return Response(user, status=200)
