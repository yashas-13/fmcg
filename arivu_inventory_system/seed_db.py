from supply_chain_system.database.core import db
from supply_chain_system.database.models import User, Product
from werkzeug.security import generate_password_hash
from supply_chain_system import create_app


def seed():
    app = create_app()
    with app.app_context():
        admin = User(username='manufacturer', password=generate_password_hash('password'), role='manufacturer')
        retailer = User(username='retailer', password=generate_password_hash('password'), role='retailer')
        db.session.add_all([admin, retailer])
        product = Product(name='Sample Product', quantity=100)
        db.session.add(product)
        db.session.commit()


if __name__ == '__main__':
    seed()
