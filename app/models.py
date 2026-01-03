import uuid
from datetime import datetime
from sqlalchemy.dialects.mysql import VARCHAR
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True) # Nullable for potential SSO later, but req says password needed
    role = db.Column(db.String(20), default='employee') # 'admin' or 'employee'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'createdAt': self.created_at.isoformat()
        }

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'createdAt': self.created_at.isoformat()
        }

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    direct_price = db.Column(db.Numeric(10, 2), default=0.0)
    unit = db.Column(db.String(20), nullable=False) # e.g., 'kg', 'pcs'
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'unitPrice': float(self.unit_price),
            'directPrice': float(self.direct_price) if self.direct_price else 0.0,
            'unit': self.unit,
            'categoryId': self.category_id,
            'createdAt': self.created_at.isoformat()
        }

class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_address = db.Column(db.Text, nullable=True)
    customer_phone = db.Column(db.String(20), nullable=True)
    
    subtotal = db.Column(db.Numeric(10, 2), default=0.0)
    gst_rate = db.Column(db.Numeric(5, 2), default=0.0)
    gst_amount = db.Column(db.Numeric(10, 2), default=0.0)
    discount = db.Column(db.Numeric(10, 2), default=0.0)
    discount_type = db.Column(db.String(20), default='percentage') # percentage or fixed
    total = db.Column(db.Numeric(10, 2), default=0.0)
    notes = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    line_items = db.relationship('InvoiceItem', backref='invoice', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'invoiceNumber': self.invoice_number,
            'date': self.date.isoformat(),
            'customer': {
                'name': self.customer_name,
                'address': self.customer_address,
                'phone': self.customer_phone
            },
            'subtotal': float(self.subtotal),
            'gstRate': float(self.gst_rate),
            'gstAmount': float(self.gst_amount),
            'discount': float(self.discount),
            'discountType': self.discount_type,
            'total': float(self.total),
            'notes': self.notes,
            'lineItems': [item.to_dict() for item in self.line_items],
            'createdAt': self.created_at.isoformat()
        }

class InvoiceItem(db.Model):
    __tablename__ = 'invoice_items'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    invoice_id = db.Column(db.String(36), db.ForeignKey('invoices.id'), nullable=False)
    
    category_id = db.Column(db.String(36), nullable=True) # Nullable for custom items
    product_id = db.Column(db.String(36), nullable=True)  # Nullable for custom items
    product_name = db.Column(db.String(200), nullable=False)
    
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    unit = db.Column(db.String(20), nullable=True)
    is_custom = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'categoryId': self.category_id,
            'productId': self.product_id,
            'productName': self.product_name,
            'quantity': float(self.quantity),
            'unitPrice': float(self.unit_price),
            'unit': self.unit,
            'isCustom': self.is_custom
        }

class Company(db.Model):
    __tablename__ = 'company_details'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(100), nullable=True)
    gst_number = db.Column(db.String(50), nullable=True)
    
    bank_account_number = db.Column(db.String(50), nullable=True)
    bank_ifsc = db.Column(db.String(20), nullable=True)
    bank_upi_id = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name or '',
            'address': self.address or '',
            'phone': self.phone or '',
            'email': self.email or '',
            'website': self.website or '',
            'gstNumber': self.gst_number or '',
            'bankDetails': {
                'accountNumber': self.bank_account_number or '',
                'ifsc': self.bank_ifsc or '',
                'upiId': self.bank_upi_id or ''
            }
        }
