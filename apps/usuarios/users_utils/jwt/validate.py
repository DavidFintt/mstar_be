from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from flask import request, jsonify
from functools import wraps
from dotenv import load_dotenv
import os
import jwt

load_dotenv()


def jwt_required(params):
    @wraps(params)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get("Authorization")
            if not token:
                raise Exception("Token não encontrado")
            token = token.split(" ")[1] if " " in token else token
            payload = jwt.decode(
                token, os.environ.get("SECRET_KEY"), algorithms=["HS256"]
            )
            return params(*args, **kwargs)
        except ExpiredSignatureError:
            raise Exception("Token expirado")
        except InvalidTokenError:
            raise Exception("Token inválido")
        except Exception as e:
            raise Exception(str(e))

    return wrapper
