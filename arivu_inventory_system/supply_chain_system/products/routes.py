from flask import Blueprint, jsonify, request
from .service import list_products, create_product

products_bp = Blueprint('products', __name__)


@products_bp.route('/', methods=['GET'])
def get_products():
    products = list_products()
    return jsonify([{'id': p.id, 'name': p.name, 'quantity': p.quantity} for p in products])


@products_bp.route('/', methods=['POST'])
def add_product():
    data = request.get_json() or {}
    name = data.get('name')
    quantity = data.get('quantity', 0)
    product = create_product(name, quantity)
    return jsonify({'id': product.id, 'name': product.name, 'quantity': product.quantity}), 201
