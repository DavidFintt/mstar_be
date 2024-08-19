from functools import wraps
from flask import jsonify, request, current_app
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from apps.usuarios.models import Users
from dotenv import load_dotenv
import os
import jwt

load_dotenv()


def is_admin(params):
    @wraps(params)
    def wrapper(*args, **kwargs):
        try:
            session = current_app.config["SESSION"]()
            token = request.headers.get("Authorization")
            token = token.split(" ")[1] if " " in token else token
            payload = jwt.decode(
                token, os.environ.get("SECRET_KEY"), algorithms=["HS256"]
            )
            user_id = payload.get("user_id")
            user = session.query(Users).filter_by(id=user_id, is_admin=True).first()
            if not user:
                raise Exception("Usuário não é administrador")
            return params(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

    return wrapper
