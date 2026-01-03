# SecureBill API Documentation

Base URL: `http://localhost:5000/api`

## Validating Connectivity
```bash
curl http://localhost:5000/health
```

---

## 1. Users API

### Get All Users
```bash
curl -X GET http://localhost:5000/api/users
```

### Create User
```bash
curl -X POST http://localhost:5000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin User",
    "email": "admin@securebill.com",
    "password": "securepassword123",
    "role": "admin"
  }'
```

### Update User
```bash
curl -X PUT http://localhost:5000/api/users/<USER_ID> \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "role": "employee"
  }'
```

### Delete User
```bash
curl -X DELETE http://localhost:5000/api/users/<USER_ID>
```

---

## 2. Categories API

### Get All Categories
```bash
curl -X GET http://localhost:5000/api/categories
```

### Create Category
```bash
curl -X POST http://localhost:5000/api/categories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electronics"
  }'
```

### Update Category
```bash
curl -X PUT http://localhost:5000/api/categories/<CATEGORY_ID> \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Home Electronics"
  }'
```

### Delete Category
```bash
curl -X DELETE http://localhost:5000/api/categories/<CATEGORY_ID>
```

---

## 3. Products API

### Get All Products
```bash
curl -X GET http://localhost:5000/api/products
```

### Create Product
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15",
    "description": "Latest Apple Smartphone",
    "unitPrice": 999.00,
    "unit": "pcs",
    "categoryId": "<CATEGORY_ID>"
  }'
```

### Update Product
```bash
curl -X PUT http://localhost:5000/api/products/<PRODUCT_ID> \
  -H "Content-Type: application/json" \
  -d '{
    "unitPrice": 899.00
  }'
```

### Delete Product
```bash
curl -X DELETE http://localhost:5000/api/products/<PRODUCT_ID>
```

---

## 4. Invoices API

### Get All Invoices
```bash
curl -X GET http://localhost:5000/api/invoices
```

### Get Single Invoice
```bash
curl -X GET http://localhost:5000/api/invoices/<INVOICE_ID>
```

### Get Next Invoice Number
```bash
curl -X GET http://localhost:5000/api/invoices/next-number
```

### Create Invoice
```bash
curl -X POST http://localhost:5000/api/invoices \
  -H "Content-Type: application/json" \
  -d '{
    "invoiceNumber": "INV-001",
    "date": "2023-10-27T10:00:00",
    "customer": {
      "name": "John Doe",
      "address": "123 Main St",
      "phone": "555-0123"
    },
    "subtotal": 1000.00,
    "gstRate": 18,
    "gstAmount": 180.00,
    "discount": 0,
    "total": 1180.00,
    "notes": "Thank you for your business",
    "lineItems": [
      {
        "productId": "<PRODUCT_ID>",
        "productName": "iPhone 15",
        "quantity": 1,
        "unitPrice": 999.00,
        "unit": "pcs",
        "categoryId": "<CATEGORY_ID>"
      },
      {
        "productName": "Screen Guard",
        "quantity": 1,
        "unitPrice": 1.00,
        "isCustom": true
      }
    ]
  }'
```

### Update Invoice (Overwrite)
```bash
curl -X PUT http://localhost:5000/api/invoices/<INVOICE_ID> \
  -H "Content-Type: application/json" \
  -d '{
    "total": 1200.00,
    "notes": "Updated Notes"
  }'
```

### Delete Invoice
```bash
curl -X DELETE http://localhost:5000/api/invoices/<INVOICE_ID>
```

---

## 5. Company Details API

### Get Company Details
```bash
curl -X GET http://localhost:5000/api/company
```

### Update Company Details
```bash
curl -X PUT http://localhost:5000/api/company \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SecureBill Inc.",
    "address": "Tech Park, City",
    "phone": "1800-123-456",
    "email": "support@securebill.com",
    "website": "www.securebill.com",
    "gstNumber": "GSTIN123456789",
    "bankDetails": {
      "accountNumber": "1234567890",
      "ifsc": "SBIN0001234",
      "upiId": "securebill@upi"
    }
  }'
```
