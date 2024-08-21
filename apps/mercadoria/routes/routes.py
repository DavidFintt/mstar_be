from flask import Blueprint, request, current_app, jsonify, session

from apps.mercadoria.models import (
    TipoMercadoria,
    Mercadoria,
    EntradaMercadoria,
    SaidaMercadoria,
)
from apps.mercadoria.schemas.mercadoria import (
    TipoMercadoriaSchema,
    MercadoriaSchema,
    EntradaMercadoriaSchema,
    SaidaMercadoriaSchema,
)
from apps.usuarios.users_utils.jwt.validate import jwt_required
from apps.mercadoria.mercadoria_utils.estoque.estoque import gerenciar_estoque
from apps.usuarios.users_utils.jwt.decode import decode_token

from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError


mercadoria_blueprint = Blueprint("mercadoria", __name__)


@mercadoria_blueprint.route("/mercadoria/tipo/", methods=["POST"])
@jwt_required
def add_tipo_mercadoria():
    try:
        db_session = current_app.config["SESSION"]()
        json_input = request.get_json()
        try:
            tipo_mercadoria_schema = TipoMercadoriaSchema()
            data = tipo_mercadoria_schema.load(json_input)
            tipo = TipoMercadoria(**data)
            db_session.add(tipo)
            db_session.commit()
            result = tipo_mercadoria_schema.dump(tipo)
            return jsonify(result), 200
        except ValidationError as e:
            return jsonify(e.messages), 500
        except SQLAlchemyError as e:
            return jsonify({"error:": str(e)}), 500
        finally:
            db_session.close()
    except Exception as e:
        return jsonify({"error:": str(e)}), 500


@mercadoria_blueprint.route("/mercadoria/register/", methods=["POST"])
@jwt_required
def register_mercadoria():
    try:
        db_session = current_app.config["SESSION"]()
        json_input = request.get_json()
        try:
            mercadoria_schema = MercadoriaSchema()
            data = mercadoria_schema.load(json_input)
            mercadoria = Mercadoria(**data)
            db_session.add(mercadoria)
            db_session.commit()
            result = mercadoria_schema.dump(mercadoria)
            return jsonify(result), 200
        except ValidationError as e:
            return jsonify(e.messages), 500
        except SQLAlchemyError as e:
            return jsonify({"error:": str(e)}), 500
        finally:
            db_session.close()
    except Exception as e:
        return jsonify({"error:": str(e)}), 500


@mercadoria_blueprint.route("/mercadoria/entrada/register/", methods=["POST"])
@jwt_required
def entrada_mercadoria():
    try:
        user = decode_token(request)
        user_id = user.get("user_id")
        db_session = current_app.config["SESSION"]()
        json_input = request.get_json()
        try:
            entrada_mercadoria_schema = EntradaMercadoriaSchema()
            data = entrada_mercadoria_schema.load(json_input)
            data["usuario"] = user_id
            entrada = EntradaMercadoria(**data)
            db_session.add(entrada)
            db_session.commit()

            result = entrada_mercadoria_schema.dump(entrada)

            # atualizar estoque
            gerenciar_estoque(data["mercadoria"], data["quantidade"], "entrada")

            return jsonify(result), 200
        except ValidationError as e:
            return jsonify(e.messages), 500
        except SQLAlchemyError as e:
            return jsonify({"error:": str(e)}), 500
        finally:
            db_session.close()
    except Exception as e:
        return jsonify({"error:": str(e)}), 500
    

@mercadoria_blueprint.route("/mercadoria/entrada/return/", methods=["GET"])
@jwt_required
def entrada_mercadoria_return():
    try:
        db_session = current_app.config["SESSION"]()
        entrada_mercadoria_schema = EntradaMercadoriaSchema()

        try:
            entrada = db_session.query(EntradaMercadoria).all()
            result = entrada_mercadoria_schema.dump(entrada, many=True)
            return jsonify(result), 200
        except ValidationError as e:
            return jsonify(e.messages), 500
        except SQLAlchemyError as e:
            return jsonify({"error:": str(e)}), 500
        finally:
            db_session.close()
    except Exception as e:
        return jsonify({"error:": str(e)}), 500

@mercadoria_blueprint.route("/mercadoria/saida/register/", methods=["POST"])
@jwt_required
def saida_mercadoria():
    try:
        user = decode_token(request)
        user_id = user.get("user_id")
        db_session = current_app.config["SESSION"]()
        json_input = request.get_json()
        try:
            saida_mercadoria_schema = SaidaMercadoriaSchema()
            data = saida_mercadoria_schema.load(json_input)
            data["usuario"] = user_id
            saida = SaidaMercadoria(**data)
            db_session.add(saida)
            db_session.commit()
            result = saida_mercadoria_schema.dump(saida)

            # atualizar estoque
            gerenciar_estoque(data["mercadoria"], data["quantidade"], "saida")

            return jsonify(result), 200
        except ValidationError as e:
            return jsonify(e.messages), 500
        except SQLAlchemyError as e:
            return jsonify({"error:": str(e)}), 500
        finally:
            db_session.close()
    except Exception as e:
        return jsonify({"error:": str(e)}), 500
    

@mercadoria_blueprint.route("/mercadoria/saida/return/", methods=["GET"])
@jwt_required
def saida_mercadoria_return():
    try:
        db_session = current_app.config["SESSION"]()
        saida_mercadoria_schema = SaidaMercadoriaSchema()

        try:
            saida = db_session.query(SaidaMercadoria).all()
            result = saida_mercadoria_schema.dump(saida, many=True)
            return jsonify(result), 200
        except ValidationError as e:
            return jsonify(e.messages), 500
        except SQLAlchemyError as e:
            return jsonify({"error:": str(e)}), 500
        finally:
            db_session.close()
    except Exception as e:
        return jsonify({"error:": str(e)}), 500


@mercadoria_blueprint.route("/mercadoria/return/", methods=["POST"])
@jwt_required
def return_mercadoria():
    try:
        db_session = current_app.config["SESSION"]()
        json_input = request.get_json()
        mercadoria_schema = MercadoriaSchema()

        try:
            if len(json_input) > 0:
                mercadoria = (
                    db_session.query(Mercadoria)
                    .filter(Mercadoria.id == json_input["mercadoria_id"])
                    .first()
                )
                result = mercadoria_schema.dump(mercadoria)
                return jsonify(result), 200
            elif len(json_input) == 0:
                mercadoria = db_session.query(Mercadoria).all()
                result = mercadoria_schema.dump(mercadoria, many=True)
                return jsonify(result), 200

            return jsonify(result), 200
        except ValidationError as e:
            return jsonify(e.messages), 500
        except SQLAlchemyError as e:
            return jsonify({"error:": str(e)}), 500
        finally:
            db_session.close()
    except Exception as e:
        return jsonify({"error:": str(e)}), 500


@mercadoria_blueprint.route("/mercadoria/tipo/return/", methods=["GET"])
@jwt_required
def tipo_mercadoria_return():
    try:
        db_session = current_app.config["SESSION"]()
        tipo_mercadoria_schema = TipoMercadoriaSchema()

        try:
            tipo = db_session.query(TipoMercadoria).all()
            result = tipo_mercadoria_schema.dump(tipo, many=True)
            return jsonify(result), 200
        except ValidationError as e:
            return jsonify(e.messages), 500
        except SQLAlchemyError as e:
            return jsonify({"error:": str(e)}), 500
        finally:
            db_session.close()
    except Exception as e:
        return jsonify({"error:": str(e)}), 500