from flask import Blueprint, request, current_app, jsonify
from apps.usuarios.users_utils.jwt.validate import jwt_required
from apps.usuarios.users_utils.validate.permissions import is_admin
from apps.unidades.schemas.unidades import UnidadeSchema
from apps.unidades.models import Unidade
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

unidade_blueprint = Blueprint("unidade", __name__)


@unidade_blueprint.route("/unidade/register/", methods=["POST"])
@jwt_required
def register_unidade():
    try:
        session = current_app.config["SESSION"]()
        json_input = request.get_json()
        try:
            unidade_schema = UnidadeSchema()
            data = unidade_schema.load(json_input)
            tipo = Unidade(**data)
            session.add(tipo)
            session.commit()
            result = unidade_schema.dump(tipo)
            return jsonify(result), 200
        except ValidationError as e:
            return jsonify(e.messages), 500
        except SQLAlchemyError as e:
            return jsonify({"error:": str(e)}), 500
        finally:
            session.close()
    except Exception as e:
        return jsonify({"error:": str(e)}), 500


@unidade_blueprint.route("/unidade/return/", methods=["GET"])
@jwt_required
def return_unidade():
    try:
        session = current_app.config["SESSION"]()
        try:
            unidade_schema = UnidadeSchema()
            unidade = session.query(Unidade).all()
            result = unidade_schema.dump(unidade, many=True)
            return jsonify(result), 200
        except ValidationError as e:
            return jsonify(e.messages), 500
        except SQLAlchemyError as e:
            return jsonify({"error:": str(e)}), 500
        finally:
            session.close()
    except Exception as e:
        return jsonify({"error:": str(e)}), 500
