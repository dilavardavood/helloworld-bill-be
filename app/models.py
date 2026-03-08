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
    sub_categories = db.relationship('SubCategory', backref='category', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'subCategories': [sc.to_dict() for sc in self.sub_categories],
            'createdAt': self.created_at.isoformat()
        }

class SubCategory(db.Model):
    __tablename__ = 'sub_categories'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='sub_category', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'categoryId': self.category_id,
            'createdAt': self.created_at.isoformat()
        }

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    retail_price = db.Column(db.Numeric(10, 2), nullable=False)
    direct_price = db.Column(db.Numeric(10, 2), default=0.0)
    gst_percentage = db.Column(db.Numeric(5, 2), default=0.0)
    unit = db.Column(db.String(20), nullable=False) # e.g., 'kg', 'pcs'
    brand_name = db.Column(db.String(100), nullable=True)
    subcategory_id = db.Column(db.String(36), db.ForeignKey('sub_categories.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'retailPrice': float(self.retail_price or 0.0),
            'directPrice': float(self.direct_price or 0.0),
            'gstPercentage': float(self.gst_percentage or 0.0),
            'unit': self.unit,
            'brandName': self.brand_name,
            'subCategoryName': self.sub_category.name if self.sub_category else None,
            'subCategoryId': self.subcategory_id,
            'categoryName': self.sub_category.category.name if self.sub_category and self.sub_category.category else None,
            'categoryId': self.sub_category.category_id if self.sub_category else None,
            'createdAt': self.created_at.isoformat()
        }

class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    retail_price = db.Column(db.Numeric(10, 2), nullable=False)
    direct_price = db.Column(db.Numeric(10, 2), default=0.0) # Labor cost
    gst_percentage = db.Column(db.Numeric(5, 2), default=0.0)
    unit = db.Column(db.String(20), nullable=False) # e.g., 'job', 'visit'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'retailPrice': float(self.retail_price or 0.0),
            'directPrice': float(self.direct_price or 0.0),
            'gstPercentage': float(self.gst_percentage or 0.0),
            'unit': self.unit,
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
    payment_received = db.Column(db.Numeric(10, 2), default=0.0)
    status = db.Column(db.String(20), default='Enquiry') # 'Enquiry', 'Confirmed', 'Completed'
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
            'subtotal': float(self.subtotal or 0),
            'gstRate': float(self.gst_rate or 0),
            'gstAmount': float(self.gst_amount or 0),
            'discount': float(self.discount or 0),
            'discountType': self.discount_type,
            'total': float(self.total or 0),
            'paymentReceived': float(self.payment_received or 0),
            'status': self.status or 'Enquiry',
            'notes': self.notes,
            'lineItems': [item.to_dict() for item in self.line_items],
            'createdAt': self.created_at.isoformat(),
            'calculatedExpense': float(sum(float(it.quantity or 0) * float(it.direct_price or 0) for it in self.line_items)),
            'calculatedProfit': float((float(self.subtotal or 0) - float(self.discount or 0)) - sum(float(it.quantity or 0) * float(it.direct_price or 0) for it in self.line_items))
        }

class InvoiceItem(db.Model):
    __tablename__ = 'invoice_items'

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    invoice_id = db.Column(db.String(36), db.ForeignKey('invoices.id'), nullable=False)
    
    subcategory_id = db.Column(db.String(36), nullable=True) # Nullable for custom items or services
    product_id = db.Column(db.String(36), nullable=True)  # Nullable for custom items or services
    service_id = db.Column(db.String(36), nullable=True) # Link to Service
    product_name = db.Column(db.String(200), nullable=False)
    
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    retail_price = db.Column(db.Numeric(10, 2), nullable=False)
    direct_price = db.Column(db.Numeric(10, 2), default=0.0)
    gst_percentage = db.Column(db.Numeric(5, 2), default=0.0)
    unit = db.Column(db.String(20), nullable=True)
    brand_name = db.Column(db.String(100), nullable=True)
    is_custom = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'subCategoryId': self.subcategory_id,
            'productId': self.product_id,
            'serviceId': self.service_id,
            'productName': self.product_name,
            'quantity': float(self.quantity),
            'retailPrice': float(self.retail_price or 0),
            'directPrice': float(self.direct_price or 0),
            'gstPercentage': float(self.gst_percentage or 0),
            'unit': self.unit,
            'brandName': self.brand_name,
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
