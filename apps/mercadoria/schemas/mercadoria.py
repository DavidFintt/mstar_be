from marshmallow import Schema, fields, pre_load, post_load
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
    numero_registro = fields.Int() 
    descricao = fields.Str(required=True)
    tipo = fields.Int(required=False)
    estoque = fields.Method("get_estoque", dump_only=True)

    @post_load
    def set_numero_registro(self, data, **kwargs):
        session = current_app.config["SESSION"]()
        count_mercadoria = session.query(Mercadoria).count()
        numero_registro = (
            str(date.today().year)
            + str(date.today().month)
            + str(date.today().day)
            + str(count_mercadoria)
        )
        data["numero_registro"] = int(numero_registro)
        return data

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
    nome_mercadoria = fields.Method("get_nome_mercadoria", dump_only=True)
    mercadoria = fields.Int(required=True)
    unidade = fields.Int(required=True)
    quantidade = fields.Int(required=True)
    usuario = fields.Int(required=False)

    def get_data_atual(self, obj):
        return datetime.now()
    
    def get_nome_mercadoria(self, obj):
        mercadoria = current_app.config["SESSION"]().query(Mercadoria).filter(Mercadoria.id == obj.mercadoria).first()
        return mercadoria.nome



class SaidaMercadoriaSchema(Schema):
    id = fields.Int(dump_only=True)
    data = fields.Method("get_data_atual", dump_only=True)
    nome_mercadoria = fields.Method("get_nome_mercadoria", dump_only=True)
    mercadoria = fields.Int(required=True)
    unidade_saida = fields.Int(required=True)
    unidade_destino = fields.Int(required=True)
    entrega = fields.Int(required=False)
    quantidade = fields.Int(required=True)
    usuario = fields.Int(required=False)

    def get_data_atual(self, obj):
        return datetime.now()
    
    def get_nome_mercadoria(self, obj):
        mercadoria = current_app.config["SESSION"]().query(Mercadoria).filter(Mercadoria.id == obj.mercadoria).first()
        return mercadoria.nome
    
