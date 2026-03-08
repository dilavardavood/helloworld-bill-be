from flask import Blueprint, request, jsonify
from app.models import Category, SubCategory
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
    
    if 'name' in data: category.name = data['name']
    
    db.session.commit()
    return jsonify(category.to_dict())

@categories_bp.route('/<id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    
    # Check if sub-categories exist
    if category.sub_categories:
        return jsonify({'error': 'Cannot delete category with existing sub-categories'}), 400
        
    db.session.delete(category)
    db.session.commit()
    return '', 204

# --- SubCategory Routes ---

@categories_bp.route('/subcategories', methods=['GET'])
def get_subcategories():
    subcategories = SubCategory.query.all()
    return jsonify([s.to_dict() for s in subcategories])

@categories_bp.route('/<category_id>/subcategories', methods=['POST'])
def create_subcategory(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Name is required'}), 400
    
    new_sub = SubCategory(name=data['name'], category_id=category.id)
    db.session.add(new_sub)
    db.session.commit()
    
    return jsonify(new_sub.to_dict()), 201

@categories_bp.route('/subcategories/<id>', methods=['PUT'])
def update_subcategory(id):
    sub = SubCategory.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data: sub.name = data['name']
    if 'categoryId' in data: sub.category_id = data['categoryId']
    
    db.session.commit()
    return jsonify(sub.to_dict())

@categories_bp.route('/subcategories/<id>', methods=['DELETE'])
def delete_subcategory(id):
    sub = SubCategory.query.get_or_404(id)
    
    # Check if products exist in this sub-category
    if sub.products:
        return jsonify({'error': 'Cannot delete sub-category with existing products'}), 400
        
    db.session.delete(sub)
    db.session.commit()
    return '', 204
