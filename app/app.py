import os
import psycopg2
import redis

from flask import Flask
from flask_restful import Resource, Api

from product.repository import PostgresRepository, RedisRepository
from product.service import ProductService
from product.view import ProductView

app = Flask(__name__)
api = Api(app)

postgres_dsn = 'postgresql://{}:{}@{}:{}/{}'.format(
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST'),
    os.getenv('DB_PORT'),
    os.getenv('DB_NAME'),
)
postgres_conn = psycopg2.connect(dsn=postgres_dsn)

redis_conn = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    password=os.getenv('REDIS_PASSWORD'),
)


class HomeView(Resource):
    def get(self):
        return 'Hello world!'


api.add_resource(HomeView, '/')
api.add_resource(ProductView, '/products', resource_class_kwargs={
    'product_service': ProductService(
        postgres_repo=PostgresRepository(postgres_conn=postgres_conn),
        redis_repo=RedisRepository(redis_conn=redis_conn),
    ),
})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
