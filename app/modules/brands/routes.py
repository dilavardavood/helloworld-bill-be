from flask import request, jsonify
from app.models import Brand
from app.extensions import db
from app.modules.brands import brands_bp

@brands_bp.route('', methods=['GET'])
def get_brands():
    brands = Brand.query.all()
    return jsonify([b.to_dict() for b in brands])

@brands_bp.route('/<id>', methods=['GET'])
def get_brand(id):
    brand = Brand.query.get_or_404(id)
    return jsonify(brand.to_dict())

@brands_bp.route('', methods=['POST'])
def create_brand():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Brand name is required'}), 400
    
    new_brand = Brand(
        name=data['name'],
        logo_url=data.get('logoUrl')
    )
    db.session.add(new_brand)
    db.session.commit()
    
    return jsonify(new_brand.to_dict()), 201

@brands_bp.route('/<id>', methods=['PUT'])
def update_brand(id):
    brand = Brand.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data: brand.name = data['name']
    if 'logoUrl' in data: brand.logo_url = data['logoUrl']
    
    db.session.commit()
    return jsonify(brand.to_dict())

@brands_bp.route('/<id>', methods=['DELETE'])
def delete_brand(id):
    brand = Brand.query.get_or_404(id)
    
    # Check if products are linked to this brand
    if brand.products:
        return jsonify({'error': 'Cannot delete brand with existing products linked to it'}), 400
        
    db.session.delete(brand)
    db.session.commit()
    return '', 204
