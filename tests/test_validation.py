from src.axentx_product.product import Product
from src.axentx_product.validation import Validation

def test_validation_init():
    validation = Validation()
    assert validation.validated_products == []

def test_validation_validate_product():
    validation = Validation()
    product = Product("Test Product", 10.99)
    assert validation.validate_product(product)
    assert len(validation.validated_products) == 1
    assert validation.validated_products[0] == product

def test_validation_invalid_product():
    validation = Validation()
    product = Product("Test Product", -1.00)
    assert not validation.validate_product(product)
    assert len(validation.validated_products) == 0
