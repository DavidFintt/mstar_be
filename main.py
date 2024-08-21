from flask import Flask, Response
from utils.db.connection.connect import db_connect
from sqlalchemy.orm import scoped_session, sessionmaker
from dotenv import load_dotenv

from apps.usuarios.routes.routes import user_blueprint
from apps.mercadoria.routes.routes import mercadoria_blueprint
from apps.cliente.routes.routes import cliente_blueprint
from apps.unidades.routes.routes import unidade_blueprint

from settings.cors import configure_cors

import jwt
import os

load_dotenv()

app = Flask(__name__)

configure_cors(app)

app.register_blueprint(user_blueprint)
app.register_blueprint(mercadoria_blueprint)
app.register_blueprint(cliente_blueprint)
app.register_blueprint(unidade_blueprint)

if __name__ == "__main__":
    engine = db_connect()
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    app.config["SESSION"] = Session
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.run(debug=True)
