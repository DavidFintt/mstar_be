from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)
    primeiro_nome = fields.Str(required=True)
    ultimo_nome = fields.Str(required=True)
    is_admin = fields.Bool(required=False)
    is_active = fields.Bool(required=False)
