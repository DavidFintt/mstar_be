import bcrypt
from apps.usuarios.models import Users
from flask import current_app


def validate_user(username, password):
    try:
        session = current_app.config["SESSION"]()
        user = session.query(Users).filter_by(email=username).first()
        if user:
            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                return user
            else:
                raise Exception("Senha incorreta")
        else:
            raise Exception("Usuário não encontrado")
    except Exception as e:
        raise Exception({"error": str(e)})
