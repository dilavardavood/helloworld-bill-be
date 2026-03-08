from app import create_app
from app.extensions import db
from sqlalchemy import inspect
import os

app = create_app(os.getenv('FLASK_ENV') or 'default')
with app.app_context():
    inspector = inspect(db.engine)
    for table_name in ['categories', 'products', 'invoices', 'invoice_items']:
        columns = [column['name'] for column in inspector.get_columns(table_name)]
        print(f"Table: {table_name}")
        print(f"Columns: {columns}")
        print("-" * 20)

    # Test insert into InvoiceItem to see exact error
    from app.models import InvoiceItem, Invoice
    import uuid
    from datetime import datetime
    
    try:
        inv = Invoice(
            invoice_number=f"DEBUG-{uuid.uuid4().hex[:6]}",
            date=datetime.utcnow(),
            customer_name="Test"
        )
        db.session.add(inv)
        db.session.flush()
        
        item = InvoiceItem(
            invoice_id=inv.id,
            product_name="Test Product",
            quantity=1,
            retail_price=100.0,
            sub_category="TestSub",
            brand_name="TestBrand"
        )
        db.session.add(item)
        db.session.commit()
        print("Test insert SUCCESS")
    except Exception as e:
        print(f"Test insert FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
