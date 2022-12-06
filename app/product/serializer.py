from marshmallow import Schema, fields


class ProductSerializer(Schema):
    id = fields.Integer()
    name = fields.String()
    price = fields.Integer()
    description = fields.String()
    quantity = fields.Integer()
