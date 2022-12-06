from flask import request
from flask_restful import Resource

from .serializer import ProductSerializer


class ProductView(Resource):
    def __init__(self, **kwargs):
        self.product_service = kwargs['product_service']
        self.product_schema = ProductSerializer()
        self.products_schema = ProductSerializer(many=True)

    def post(self):
        json_user = request.get_json()
        product = self.product_schema.load(json_user)

        errors = []
        if product.get('name') is None:
            errors.append({
                'name': 'field name is required.',
            })

        if product.get('price') is None or not isinstance(product.get('price'), int):
            errors.append({
                'price': 'field price must be integer and required.'
            })

        if product.get('quantity') is None or not isinstance(product.get('quantity'), int):
            errors.append({
                'quantity': 'field quantity must be integer and required.'
            })

        if len(errors) > 0:
            return {
                'status': 'error',
                'message': 'Fields validation failed.',
                'errors': errors,
            }

        ok = self.product_service.add_product({
            'name': str(product.get('name')),
            'price': int(product.get('price', 0)),
            'description': str(product.get('description', '')),
            'quantity': int(product.get('quantity', 0)),
        })

        if not ok:
            return {
                'status': 'error',
                'message': 'Internal server error.'
            }

        return {
            'status': 'ok',
            'message': 'Successfully create new product.'
        }

    def get(self):
        sort_by = request.args.get('sort_by')
        sort_dir = request.args.get('sort_dir')

        if sort_by is None or sort_by not in ('id', 'price', 'name'):
            sort_by = 'id'

        if sort_dir is None or sort_dir not in ('asc', 'desc'):
            sort_dir = 'desc'

        list_products = self.product_service.list_products(sort_by, sort_dir)
        return {
            'status': 'ok',
            'message': 'Successfully fetch products.',
            'data': self.products_schema.dump(list_products)
        }
