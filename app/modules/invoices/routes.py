from flask import Blueprint, request, jsonify
from app.models import Invoice, InvoiceItem
from app.extensions import db
from datetime import datetime
import re

invoices_bp = Blueprint('invoices', __name__)

@invoices_bp.route('', methods=['GET'])
def get_invoices():
    invoices = Invoice.query.order_by(Invoice.created_at.desc()).all()
    return jsonify([inv.to_dict() for inv in invoices])

@invoices_bp.route('/<id>', methods=['GET'])
def get_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    return jsonify(invoice.to_dict())

@invoices_bp.route('/next-number', methods=['GET'])
def get_next_number():
    # Simple logic: INV-{count+1} or find global max.
    # We will try to parse the last invoice number to increment it.
    last_invoice = Invoice.query.order_by(Invoice.created_at.desc()).first()
    
    if not last_invoice:
        return jsonify({'nextNumber': 'INV-001'})
    
    # Try to extract number
    match = re.search(r'(\d+)$', last_invoice.invoice_number)
    if match:
        num = int(match.group(1)) + 1
        prefix = last_invoice.invoice_number[:match.start()]
        # Preserve padding if present in original (simple assumption: 3 digits)
        new_num_str = f"{num:03d}"
        return jsonify({'nextNumber': f"{prefix}{new_num_str}"})
    
    # Fallback
    return jsonify({'nextNumber': f"{last_invoice.invoice_number}-1"})

@invoices_bp.route('', methods=['POST'])
def create_invoice():
    data = request.get_json()
    if not data or not data.get('invoiceNumber') or not data.get('lineItems'):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Create Invoice
        invoice = Invoice(
            invoice_number=data['invoiceNumber'],
            date=datetime.fromisoformat(data['date'].replace('Z', '+00:00')) if 'date' in data else datetime.utcnow(),
            customer_name=data.get('customer', {}).get('name'),
            customer_address=data.get('customer', {}).get('address'),
            customer_phone=data.get('customer', {}).get('phone'),
            subtotal=data.get('subtotal', 0),
            gst_rate=data.get('gstRate', 0),
            gst_amount=data.get('gstAmount', 0),
            discount=data.get('discount', 0),
            discount_type=data.get('discountType', 'percentage'),
            total=data.get('total', 0),
            notes=data.get('notes')
        )
        
        db.session.add(invoice)
        db.session.flush() # Get ID

        # Create Line Items
        for item_data in data['lineItems']:
            item = InvoiceItem(
                invoice_id=invoice.id,
                category_id=item_data.get('categoryId'),
                product_id=item_data.get('productId'),
                product_name=item_data['productName'],
                quantity=item_data['quantity'],
                unit_price=item_data['unitPrice'],
                unit=item_data.get('unit'),
                is_custom=item_data.get('isCustom', False)
            )
            db.session.add(item)
        
        db.session.commit()
        return jsonify(invoice.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@invoices_bp.route('/<id>', methods=['PUT'])
def update_invoice(id):
    # For invoices, usually full update or specific status update.
    # We'll allow updating basic fields and line items (replace all).
    invoice = Invoice.query.get_or_404(id)
    data = request.get_json()

    try:
        if 'invoiceNumber' in data: invoice.invoice_number = data['invoiceNumber']
        if 'customer' in data:
            invoice.customer_name = data['customer'].get('name', invoice.customer_name)
            invoice.customer_address = data['customer'].get('address', invoice.customer_address)
            invoice.customer_phone = data['customer'].get('phone', invoice.customer_phone)
        
        if 'total' in data: invoice.total = data['total']
        # ... map other fields as necessary
        
        # If lineItems provided, replace them?
        # Standard approach: delete all and recreate, or diff.
        # Requirement: "Transactional".
        if 'lineItems' in data:
            InvoiceItem.query.filter_by(invoice_id=invoice.id).delete()
            for item_data in data['lineItems']:
                item = InvoiceItem(
                    invoice_id=invoice.id,
                    category_id=item_data.get('categoryId'),
                    product_id=item_data.get('productId'),
                    product_name=item_data['productName'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unitPrice'],
                    unit=item_data.get('unit'),
                    is_custom=item_data.get('isCustom', False)
                )
                db.session.add(item)
        
        db.session.commit()
        return jsonify(invoice.to_dict())
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@invoices_bp.route('/<id>', methods=['DELETE'])
def delete_invoice(id):
    invoice = Invoice.query.get_or_404(id)
    db.session.delete(invoice)
    # Line items deleted by cascade in model? No, I added 'cascade="all, delete-orphan"' to the db.relationship(Invoice.line_items)
    # Wait, in models.py I put cascade on the relationship in Invoice model.
    db.session.commit()
    return '', 204
