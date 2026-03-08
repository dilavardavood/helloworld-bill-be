from flask import Blueprint, request, jsonify
from app.models import Service
from app.extensions import db

services_bp = Blueprint('services', __name__)

@services_bp.route('', methods=['GET'])
def get_services():
    services = Service.query.all()
    return jsonify([s.to_dict() for s in services])

@services_bp.route('/<id>', methods=['GET'])
def get_service(id):
    service = Service.query.get_or_404(id)
    return jsonify(service.to_dict())

@services_bp.route('', methods=['POST'])
def create_service():
    data = request.get_json()
    required = ['name', 'retailPrice', 'unit']
    if not data or any(field not in data for field in required):
        return jsonify({'error': 'Missing required fields: name, retailPrice, unit'}), 400
    
    new_service = Service(
        name=data['name'],
        description=data.get('description'),
        retail_price=data['retailPrice'],
        direct_price=data.get('directPrice', 0.0),
        gst_percentage=data.get('gstPercentage', 0.0),
        unit=data['unit']
    )
    db.session.add(new_service)
    db.session.commit()
    return jsonify(new_service.to_dict()), 201

@services_bp.route('/<id>', methods=['PUT'])
def update_service(id):
    service = Service.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data: service.name = data['name']
    if 'description' in data: service.description = data['description']
    if 'retailPrice' in data: service.retail_price = data['retailPrice']
    if 'directPrice' in data: service.direct_price = data['directPrice']
    if 'gstPercentage' in data: service.gst_percentage = data['gstPercentage']
    if 'unit' in data: service.unit = data['unit']
    
    db.session.commit()
    return jsonify(service.to_dict())

@services_bp.route('/<id>', methods=['DELETE'])
def delete_service(id):
    service = Service.query.get_or_404(id)
    # Note: In a real system, you might want to check if service appears in invoices before deleting.
    db.session.delete(service)
    db.session.commit()
    return '', 204
