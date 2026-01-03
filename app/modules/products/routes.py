from flask import Blueprint, request, jsonify
from app.models import Product, Category
from app.extensions import db

products_bp = Blueprint('products', __name__)

@products_bp.route('', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@products_bp.route('', methods=['POST'])
def create_product():
    data = request.get_json()
    required = ['name', 'unitPrice', 'unit']
    if not data or any(field not in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_product = Product(
        name=data['name'],
        description=data.get('description'),
        unit_price=data['unitPrice'],
        direct_price=data.get('directPrice', 0.0),
        unit=data['unit'],
        category_id=data.get('categoryId')
    )
    
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify(new_product.to_dict()), 201

@products_bp.route('/<id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data: product.name = data['name']
    if 'description' in data: product.description = data['description']
    if 'unitPrice' in data: product.unit_price = data['unitPrice']
    if 'directPrice' in data: product.direct_price = data['directPrice']
    if 'unit' in data: product.unit = data['unit']
    if 'categoryId' in data: product.category_id = data['categoryId']
    
    db.session.commit()
    return jsonify(product.to_dict())

@products_bp.route('/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204
