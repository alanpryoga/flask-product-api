from .model import Product


class ProductService:
    def __init__(self, postgres_repo, redis_repo):
        self.postgres_repo = postgres_repo
        self.redis_repo = redis_repo

    def add_product(self, product):
        ok = self.postgres_repo.add_product(product)
        if ok:
            self.redis_repo.clear_list_products()
            return True
        return False

    def list_products(self, sort_by, sort_dir):
        redis_key = 'list_products:{}:{}'.format(sort_by, sort_dir)

        products = self.redis_repo.get_list_products(redis_key)
        if products is None:
            products = self.postgres_repo.list_products(sort_by, sort_dir)
            self.redis_repo.set_list_products(redis_key, products)

        result = []
        for product in products:
            result.append(Product(
                id=product.get('id'),
                name=product.get('name'),
                price=product.get('price'),
                description=product.get('description'),
                quantity=product.get('quantity'),
            ))

        return result
