import json
import re
from datetime import timedelta


class PostgresRepository:
    def __init__(self, postgres_conn):
        self.postgres_conn = postgres_conn

    def add_product(self, product):
        query = 'INSERT INTO products (name, price, description, quantity) VALUES (%s, %s, %s, %s)'

        cursor = self.postgres_conn.cursor()
        cursor.execute(query, (
            product.get('name'),
            product.get('price'),
            product.get('description'),
            product.get('quantity'),
        ))
        self.postgres_conn.commit()

        rowcount = cursor.rowcount
        if rowcount > 0:
            return True
        return False

    def list_products(self, sort_by, sort_dir):
        clean_sort_by = re.sub(r'[^\w]', '', sort_by)
        clean_sort_dir = re.sub(r'[^\w]', '', sort_dir)

        query = 'SELECT id, name, price, description, quantity FROM products ORDER BY {} {}'.format(
            clean_sort_by,
            clean_sort_dir.upper()
        )

        cursor = self.postgres_conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        result = []
        for row in rows:
            item = {
                'id': row[0],
                'name': row[1],
                'price': row[2],
                'description': row[3],
                'quantity': row[4],
            }
            result.append(item)
        return result


class RedisRepository:
    def __init__(self, redis_conn):
        self.redis_conn = redis_conn

    def get_list_products(self, redis_key):
        json_list_products = self.redis_conn.get(redis_key)
        if json_list_products is None:
            return None
        list_products = json.loads(self.redis_conn.get(redis_key))
        return list_products

    def set_list_products(self, redis_key, list_products):
        json_list_products = json.dumps(list_products)
        self.redis_conn.setex(redis_key, timedelta(minutes=5), value=json_list_products)

    def clear_list_products(self):
        self.redis_conn.flushdb()
