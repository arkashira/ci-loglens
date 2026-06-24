from src.axentx_product.portfolio import Portfolio
from src.axentx_product.product import Product

def test_portfolio_init():
    portfolio = Portfolio()
    assert portfolio.products == []

def test_portfolio_add_product():
    portfolio = Portfolio()
    product = Product("Test Product", 10.99)
    portfolio.add_product(product)
    assert len(portfolio.products) == 1
    assert portfolio.products[0] == product

def test_portfolio_get_products():
    portfolio = Portfolio()
    product1 = Product("Test Product 1", 10.99)
    product2 = Product("Test Product 2", 9.99)
    portfolio.add_product(product1)
    portfolio.add_product(product2)
    products = portfolio.get_products()
    assert len(products) == 2
    assert products[0] == product1
    assert products[1] == product2
