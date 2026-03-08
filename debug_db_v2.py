from app import create_app
from app.extensions import db
import os
import uuid
from datetime import datetime

app = create_app(os.getenv('FLASK_ENV') or 'default')
with app.app_context():
    from app.models import InvoiceItem, Invoice, Product
    
    try:
        # Create a test product
        prod = Product(
            name="Debug Product",
            retail_price=999.0,
            unit="pcs",
            sub_category="DebugSub",
            brand_name="DebugBrand"
        )
        db.session.add(prod)
        db.session.flush()
        print(f"Product created: {prod.id}")

        inv = Invoice(
            invoice_number=f"DEBUG-V-{uuid.uuid4().hex[:6]}",
            date=datetime.utcnow(),
            customer_name="Test"
        )
        db.session.add(inv)
        db.session.flush()
        print(f"Invoice created: {inv.id}")
        
        # This matches the verify script's payload logic
        item_data = {
            "productId": prod.id,
            "productName": "Debug Product",
            "quantity": 1,
            "retailPrice": 999.00
        }

        d_price = item_data.get('directPrice')
        if d_price is None and item_data.get('productId'):
            product = Product.query.get(item_data['productId'])
            if product:
                d_price = float(product.direct_price)
                if 'subCategory' not in item_data: item_data['subCategory'] = product.sub_category
                if 'brandName' not in item_data: item_data['brandName'] = product.brand_name
        
        print(f"Determined directPrice={d_price}, subCategory={item_data.get('subCategory')}, brandName={item_data.get('brandName')}")

        item = InvoiceItem(
            invoice_id=inv.id,
            category_id=item_data.get('categoryId'),
            product_id=item_data.get('productId'),
            product_name=item_data['productName'],
            quantity=item_data['quantity'],
            retail_price=item_data['retailPrice'],
            direct_price=d_price or 0.0,
            gst_percentage=item_data.get('gstPercentage', 0.0),
            unit=item_data.get('unit'),
            sub_category=item_data.get('subCategory'),
            brand_name=item_data.get('brandName'),
            is_custom=item_data.get('isCustom', False)
        )
        db.session.add(item)
        db.session.commit()
        print("Test complex insert SUCCESS")
    except Exception as e:
        print(f"Test complex insert FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
