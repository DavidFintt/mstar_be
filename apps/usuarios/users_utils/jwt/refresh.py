from dotenv import load_dotenv
from flask import current_app
from datetime import datetime, timedelta, timezone
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from apps.usuarios.models import Users
import os
import jwt

load_dotenv()


def refresh(refresh_token):
    try:
        session = current_app.config["SESSION"]()
        payload = jwt.decode(
            refresh_token, os.environ.get("SECRET_KEY"), algorithms=["HS256"]
        )
        user = session.query(Users).filter_by(id=payload.get("user_id")).first()
        access_payload = {
            "user_id": user.id,
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
            "iat": datetime.now(timezone.utc),
            "sub": user.email,
        }

        access_token = jwt.encode(
            access_payload, os.environ.get("SECRET_KEY"), algorithm="HS256"
        )
        return {"access_token": access_token}
    except ExpiredSignatureError:
        raise Exception("Token expirado")
    except InvalidTokenError:
        raise Exception("Token inválido")
    except Exception as e:
        raise Exception({"error": str(e)})
