from src.axentx_product.product import Product

def test_product_init():
    product = Product("Test Product", 10.99)
    assert product.name == "Test Product"
    assert product.price == 10.99

def test_product_str():
    product = Product("Test Product", 10.99)
    assert str(product) == "Test Product: $10.99"
