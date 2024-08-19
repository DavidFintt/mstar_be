from marshmallow import Schema, fields
from flask import current_app, session
from apps.mercadoria.models import Mercadoria
from datetime import date, datetime
from apps.mercadoria.models import Mercadoria, EstoqueMercadoria


class TipoMercadoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    descricao = fields.Str(required=True)


class MercadoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True)
    fabricante = fields.Str(required=True, load_only=True)
    numero_registro = fields.Method("get_numero_registro", dump_only=True)
    descricao = fields.Str(required=True)
    tipo = fields.Int(required=False)
    estoque = fields.Method("get_estoque", dump_only=True)

    def get_numero_registro(self, obj):
        session = current_app.config["SESSION"]()
        count_mercadoria = session.query(Mercadoria).count()
        numero_registro = (
            str(date.today().year)
            + str(date.today().month)
            + str(date.today().day)
            + str(count_mercadoria)
        )

        return int(numero_registro)

    def get_estoque(self, obj):
        session = current_app.config["SESSION"]()
        estoque = (
            session.query(EstoqueMercadoria)
            .filter(EstoqueMercadoria.mercadoria == obj.id)
            .first()
        )
        if estoque:
            return estoque.quantidade
        return 0


class EntradaMercadoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    data = fields.Method("get_data_atual", dump_only=True)
    mercadoria = fields.Int(required=True)
    unidade = fields.Int(required=True)
    quantidade = fields.Int(required=True)

    def get_data_atual(self, obj):
        return datetime.now()


class SaidaMercadoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    data = fields.Method("get_data_atual", dump_only=True)
    mercadoria = fields.Int(required=True)
    unidade_saida = fields.Int(required=True)
    unidade_destino = fields.Int(required=True)
    entrega = fields.Int(required=False)
    quantidade = fields.Int(required=True)

    def get_data_atual(self, obj):
        return datetime.now()
