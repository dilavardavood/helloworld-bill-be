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
    required = ['name', 'retailPrice', 'unit']
    if not data or any(field not in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_product = Product(
        name=data['name'],
        description=data.get('description'),
        retail_price=data['retailPrice'],
        direct_price=data.get('directPrice', 0.0),
        gst_percentage=data.get('gstPercentage', 0.0),
        unit=data['unit'],
        brand_name=data.get('brandName'),
        subcategory_id=data.get('subCategoryId')
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
    if 'retailPrice' in data: product.retail_price = data['retailPrice']
    if 'directPrice' in data: product.direct_price = data['directPrice']
    if 'gstPercentage' in data: product.gst_percentage = data['gstPercentage']
    if 'unit' in data: product.unit = data['unit']
    if 'brandName' in data: product.brand_name = data['brandName']
    if 'subCategoryId' in data: product.subcategory_id = data['subCategoryId']
    
    db.session.commit()
    return jsonify(product.to_dict())

@products_bp.route('/<id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204
