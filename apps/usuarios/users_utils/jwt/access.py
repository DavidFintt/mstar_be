import jwt
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os

load_dotenv()


def generate_token(user):
    try:
        access_payload = {
            "user_id": user.id,
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "sub": user.email,
        }

        refresh_payload = {
            "user_id": user.id,
            "exp": datetime.now(timezone.utc) + timedelta(days=7),
            "iat": datetime.now(timezone.utc),
            "sub": user.email,
        }

        access_token = jwt.encode(
            access_payload, os.environ.get("SECRET_KEY"), algorithm="HS256"
        )

        refresh_token = jwt.encode(
            refresh_payload, os.environ.get("SECRET_KEY"), algorithm="HS256"
        )
        return {"access_token": access_token, "refresh_token": refresh_token}

    except Exception as e:
        raise Exception({"error": str(e)})
