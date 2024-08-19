from flask import Response, Blueprint, request, current_app, jsonify
from apps.cliente.models import Cliente
from apps.mercadoria.models import TipoMercadoria, Mercadoria
from apps.cliente.schemas.cliente import ClienteSchema
from apps.usuarios.users_utils.jwt.validate import jwt_required
from apps.usuarios.users_utils.validate.permissions import is_admin
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

cliente_blueprint = Blueprint("cliente", __name__)


@cliente_blueprint.route("/cliente/register/", methods=["POST"])
@jwt_required
def registro_cliente():
    try:
        session = current_app.config["SESSION"]()
        json_input = request.get_json()
        try:
            cliente_schema = ClienteSchema()
            data = cliente_schema.load(json_input)
            tipo = Cliente(**data)
            session.add(tipo)
            session.commit()
            result = cliente_schema.dump(tipo)
            return jsonify(result), 200
        except ValidationError as e:
            return jsonify(e.messages), 500
        except SQLAlchemyError as e:
            return jsonify({"error:": str(e)}), 500
        finally:
            session.close()
    except Exception as e:
        return jsonify({"error:": str(e)}), 500
