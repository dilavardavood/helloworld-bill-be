from app import create_app
from app.extensions import db
import os

app = create_app(os.getenv('FLASK_ENV') or 'default')
with app.app_context():
    print("🧹 Clearing database...")
    try:
        # Delete in order of dependencies
        from app.models import InvoiceItem, Invoice, Product, Category
        
        print("Deleting InvoiceItems...")
        db.session.query(InvoiceItem).delete()
        print("Deleting Invoices...")
        db.session.query(Invoice).delete()
        print("Deleting Products...")
        db.session.query(Product).delete()
        print("Deleting Categories...")
        db.session.query(Category).delete()
        
        db.session.commit()
        print("✨ Database cleared successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error clearing database: {str(e)}")
        import traceback
        traceback.print_exc()
