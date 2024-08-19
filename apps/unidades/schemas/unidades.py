from marshmallow import Schema, fields, validate


class UnidadeSchema(Schema):
    id = fields.Int(dump_only=True)
    nome = fields.Str(required=True, validate=validate.Length(max=50))
    cidade = fields.Str(required=True, validate=validate.Length(max=50))
    uf = fields.Str(required=True, validate=validate.Length(max=2))
    endereco = fields.Str(required=True, validate=validate.Length(max=50))
