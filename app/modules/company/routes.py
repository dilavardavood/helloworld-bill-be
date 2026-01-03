from flask import Blueprint, request, jsonify
from app.models import Company
from app.extensions import db

company_bp = Blueprint('company', __name__)

@company_bp.route('', methods=['GET'])
def get_company():
    company = Company.query.first()
    if not company:
        # Return empty structure if not set
        return jsonify({}) 
    return jsonify(company.to_dict())

@company_bp.route('', methods=['PUT'])
def update_company():
    company = Company.query.first()
    data = request.get_json()
    
    if not company:
        company = Company()
        db.session.add(company)
    
    if 'name' in data: company.name = data['name']
    if 'address' in data: company.address = data['address']
    if 'phone' in data: company.phone = data['phone']
    if 'email' in data: company.email = data['email']
    if 'website' in data: company.website = data['website']
    if 'gstNumber' in data: company.gst_number = data['gstNumber']
    
    bank_details = data.get('bankDetails', {})
    if 'accountNumber' in bank_details: company.bank_account_number = bank_details['accountNumber']
    if 'ifsc' in bank_details: company.bank_ifsc = bank_details['ifsc']
    if 'upiId' in bank_details: company.bank_upi_id = bank_details['upiId']
    
    db.session.commit()
    return jsonify(company.to_dict())
