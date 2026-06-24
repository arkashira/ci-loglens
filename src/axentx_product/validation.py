from .product import Product

class Validation:
    def __init__(self):
        self.validated_products = []

    def validate_product(self, product):
        # Simple validation: price must be greater than 0
        if product.price > 0:
            self.validated_products.append(product)
            return True
        return False
