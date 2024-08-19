from marshmallow import Schema, fields, validate


class ClienteSchema(Schema):
    id = fields.Int(dump_only=True)
    primeiro_nome = fields.Str(required=True, validate=validate.Length(max=20))
    ultimo_nome = fields.Str(required=True, validate=validate.Length(max=20))
    cpf = fields.Str(required=True, validate=validate.Length(max=11))
    telefone = fields.Str(required=True, validate=validate.Length(max=11))
    email = fields.Email(required=True, validate=validate.Email())
    cep = fields.Str(required=True, validate=validate.Length(max=8))
    cidade = fields.Str(required=True, validate=validate.Length(max=50))
    uf = fields.Str(required=True, validate=validate.Length(max=2))
    endereco = fields.Str(required=True, validate=validate.Length(max=50))
