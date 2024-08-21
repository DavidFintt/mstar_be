from dotenv import load_dotenv
import jwt
import os

load_dotenv()

def decode_token(request):
    try:
        token = request.headers.get("Authorization")
        if not token:
                raise Exception("Token não encontrado")
        token = token.split(" ")[1] if " " in token else token
        payload = jwt.decode(
            token, os.environ.get("SECRET_KEY"), algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expirado!"
    except jwt.InvalidTokenError:
        return "Token inválido!"