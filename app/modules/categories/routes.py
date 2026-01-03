from flask import Blueprint, request, jsonify
from app.models import Category
from app.extensions import db

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])

@categories_bp.route('', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    
    return jsonify(new_category.to_dict()), 201

@categories_bp.route('/<id>', methods=['PUT'])
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data:
        category.name = data['name']
        db.session.commit()
        
    return jsonify(category.to_dict())

@categories_bp.route('/<id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    
    # Check if products exist
    if category.products:
        return jsonify({'error': 'Cannot delete category with existing products'}), 400
        
    db.session.delete(category)
    db.session.commit()
    return '', 204
