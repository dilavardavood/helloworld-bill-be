from flask import Blueprint, request, jsonify
from app.models import Invoice, InvoiceItem, Product, Service
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

def _generate_next_invoice_number():
    last_invoice = Invoice.query.order_by(Invoice.created_at.desc()).first()
    
    if not last_invoice:
        return 'INV-001'
    
    # Try to extract number
    match = re.search(r'(\d+)$', last_invoice.invoice_number)
    if match:
        num = int(match.group(1)) + 1
        prefix = last_invoice.invoice_number[:match.start()]
        # Preserve padding (e.g. 001 -> 002)
        padding = len(match.group(1))
        new_num_str = f"{num:0{padding}d}"
        return f"{prefix}{new_num_str}"
    
    # Fallback
    return f"{last_invoice.invoice_number}-1"

@invoices_bp.route('/next-number', methods=['GET'])
def get_next_number():
    return jsonify({'nextNumber': _generate_next_invoice_number()})

@invoices_bp.route('/analytics', methods=['GET'])
def get_analytics():
    from sqlalchemy import extract
    
    month = request.args.get('month', type=int)
    year = request.args.get('year', type=int)
    
    query = Invoice.query
    
    if year:
        query = query.filter(extract('year', Invoice.date) == year)
    if month:
        query = query.filter(extract('month', Invoice.date) == month)
        
    query = query.filter(Invoice.status == 'Completed')
    invoices = query.all()
    
    total_revenue = 0.0
    total_expense = 0.0
    
    for inv in invoices:
        subtotal = float(inv.subtotal or 0)
        discount = float(inv.discount or 0)
        total_revenue += (subtotal - discount)
        
        for item in inv.line_items:
            qty = float(item.quantity or 0)
            d_price = float(item.direct_price or 0)
            total_expense += (qty * d_price)
    
    total_profit = total_revenue - total_expense
    
    return jsonify({
        'totalBills': len(invoices),
        'totalRevenue': total_revenue,
        'totalExpense': total_expense,
        'totalProfit': total_profit
    })

@invoices_bp.route('', methods=['POST'])
def create_invoice():
    data = request.get_json()
    if not data or not data.get('lineItems'):
        return jsonify({'error': 'Missing required fields (lineItems)'}), 400

    try:
        inv_number = data.get('invoiceNumber') or _generate_next_invoice_number()
        
        # Create Invoice
        invoice = Invoice(
            invoice_number=inv_number,
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
            payment_received=data.get('paymentReceived', 0.0),
            status=data.get('status', 'Enquiry'),
            notes=data.get('notes')
        )
        
        db.session.add(invoice)
        db.session.flush() # Get ID

        # Create Line Items
        for item_data in data['lineItems']:
            # Determine direct price
            d_price = item_data.get('directPrice')
            if d_price is None and item_data.get('productId'):
                product = Product.query.get(item_data['productId'])
                if product:
                    d_price = float(product.direct_price)
                    if 'subCategoryId' not in item_data: item_data['subCategoryId'] = product.subcategory_id
                    if 'brandName' not in item_data: item_data['brandName'] = product.brand_name
            elif d_price is None and item_data.get('serviceId'):
                service = Service.query.get(item_data['serviceId'])
                if service:
                    d_price = float(service.direct_price)
            
            item = InvoiceItem(
                invoice_id=invoice.id,
                subcategory_id=item_data.get('subCategoryId'),
                subcategory_name=item_data.get('subCategoryName'),
                product_id=item_data.get('productId'),
                service_id=item_data.get('serviceId'),
                product_name=item_data['productName'],
                category_name=item_data.get('categoryName'),
                quantity=item_data['quantity'],
                retail_price=item_data['retailPrice'],
                direct_price=d_price or 0.0,
                gst_percentage=item_data.get('gstPercentage', 0.0),
                unit=item_data.get('unit'),
                brand_name=item_data.get('brandName'),
                is_custom=item_data.get('isCustom', False)
            )
            db.session.add(item)
        
        db.session.commit()
        return jsonify(invoice.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
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
        if 'paymentReceived' in data: invoice.payment_received = data['paymentReceived']
        if 'status' in data: invoice.status = data['status']
        # ... map other fields as necessary
        
        # If lineItems provided, replace them?
        # Standard approach: delete all and recreate, or diff.
        # Requirement: "Transactional".
        if 'lineItems' in data:
            InvoiceItem.query.filter_by(invoice_id=invoice.id).delete()
            for item_data in data['lineItems']:
                # Determine direct price
                d_price = item_data.get('directPrice')
                if d_price is None and item_data.get('productId'):
                    product = Product.query.get(item_data['productId'])
                    if product:
                        d_price = float(product.direct_price)
                        if 'subCategoryId' not in item_data: item_data['subCategoryId'] = product.subcategory_id
                        if 'brandName' not in item_data: item_data['brandName'] = product.brand_name
                elif d_price is None and item_data.get('serviceId'):
                    service = Service.query.get(item_data['serviceId'])
                    if service:
                        d_price = float(service.direct_price)

                item = InvoiceItem(
                    invoice_id=invoice.id,
                    subcategory_id=item_data.get('subCategoryId'),
                    subcategory_name=item_data.get('subCategoryName'),
                    product_id=item_data.get('productId'),
                    service_id=item_data.get('serviceId'),
                    product_name=item_data['productName'],
                    category_name=item_data.get('categoryName'),
                    quantity=item_data['quantity'],
                    retail_price=item_data['retailPrice'],
                    direct_price=d_price or 0.0,
                    gst_percentage=item_data.get('gstPercentage', 0.0),
                    unit=item_data.get('unit'),
                    brand_name=item_data.get('brandName'),
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
