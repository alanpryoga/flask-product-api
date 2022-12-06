class Product:
    def __init__(self, id, name, price, description, quantity):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def __repr__(self):
        return '<Product %s>'.format(self.name)
