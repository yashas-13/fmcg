from ..database.models import Product
from ..database.core import db


def list_products() -> list[Product]:
    return Product.query.all()


def create_product(name: str, quantity: int = 0) -> Product:
    product = Product(name=name, quantity=quantity)
    db.session.add(product)
    db.session.commit()
    return product
