# SecureBill API Documentation

Base URL: `http://localhost:5000/api`

## Validating Connectivity
```bash
curl http://localhost:5000/health
```
*Returns the status of the server.*

---

## 1. Users API

### Get All Users
*Retrieve a list of all registered users.*
```bash
curl -X GET http://localhost:5000/api/users
```

### Create User
*Create a new user account (admin or employee).*
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
*Modify details of an existing user.*
```bash
curl -X PUT http://localhost:5000/api/users/<USER_ID> \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Name",
    "role": "employee"
  }'
```

### Delete User
*Permanently remove a user from the system.*
```bash
curl -X DELETE http://localhost:5000/api/users/<USER_ID>
```

---

## 2. Categories API

### Get All Categories
*Retrieve all product categories with their sub-categories.*
```bash
curl -X GET http://localhost:5000/api/categories
```

### Create Category
*Create a new top-level category.*
```bash
curl -X POST http://localhost:5000/api/categories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CCTV Cameras"
  }'
```

### Create Sub-Category
*Create a sub-category under a parent category.*
```bash
curl -X POST http://localhost:5000/api/categories/<CATEGORY_ID>/subcategories \
  -H "Content-Type: application/json" \
  -d '{
    "name": "IP Dome"
  }'
```

### Update Sub-Category
*Modify a sub-category's name or move it to a different parent category.*
```bash
curl -X PUT http://localhost:5000/api/categories/subcategories/<SUBCATEGORY_ID> \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated SubCategory Name",
    "categoryId": "<NEW_CATEGORY_ID>"
  }'
```

### Delete Category
*Delete a category (ensure no products are linked).*
```bash
curl -X DELETE http://localhost:5000/api/categories/<CATEGORY_ID>
```

---

## 3. Products API

### Get All Products
*Retrieve all available products with pricing and GST details.*
```bash
curl -X GET http://localhost:5000/api/products
```

### Create Product
*Add a new product linked to a sub-category.*
```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hikvision 4MP IP Dome",
    "description": "High resolution night vision camera",
    "retailPrice": 3800.00,
    "directPrice": 2900.00,
    "gstPercentage": 18.0,
    "unit": "nos",
    "brandId": "<BRAND_ID>",
    "subCategoryId": "<SUBCATEGORY_ID>",
    "imageUrl": "https://example.com/product-image.png",
    "modelNumber": "MODEL-123",
    "serialNumber": "SN-456"
  }'
```

### Update Product
*Update product pricing, GST, or descriptions.*
```bash
curl -X PUT http://localhost:5000/api/products/<PRODUCT_ID> \
  -H "Content-Type: application/json" \
  -d '{
    "retailPrice": 899.00,
    "gstPercentage": 12.0
  }'
```

### Delete Product
*Remove a product from the inventory.*
```bash
curl -X DELETE http://localhost:5000/api/products/<PRODUCT_ID>
```

---

## 4. Brands API

### Get All Brands
*Retrieve a list of all brands.*
```bash
curl -X GET http://localhost:5000/api/brands
```

### Get Single Brand
*Retrieve details for a specific brand.*
```bash
curl -X GET http://localhost:5000/api/brands/<BRAND_ID>
```

### Create Brand
*Create a new brand.*
```bash
curl -X POST http://localhost:5000/api/brands \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Hikvision",
    "logoUrl": "https://example.com/hikvision-logo.png"
  }'
```

### Update Brand
*Modify brand details.*
```bash
curl -X PUT http://localhost:5000/api/brands/<BRAND_ID> \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Brand Name",
    "logoUrl": "https://example.com/new-logo.png"
  }'
```

### Delete Brand
*Delete a brand (ensure no products are linked).*
```bash
curl -X DELETE http://localhost:5000/api/brands/<BRAND_ID>
```

---

## 5. Services API

### Get All Services
*Retrieve all available services (Installation, Maintenance, etc.).*
```bash
curl -X GET http://localhost:5000/api/services
```

### Create Service
*Add a new service with pricing and GST.*
```bash
curl -X POST http://localhost:5000/api/services \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CCTV Installation",
    "description": "Installation and configuration of 4 cameras",
    "retailPrice": 3000.00,
    "directPrice": 1500.00,
    "gstPercentage": 18.0,
    "unit": "job"
  }'
```

### Update Service
*Modify service details or pricing.*
```bash
curl -X PUT http://localhost:5000/api/services/<SERVICE_ID> \
  -H "Content-Type: application/json" \
  -d '{
    "retailPrice": 3500.00
  }'
```

### Delete Service
*Remove a service from the catalog.*
```bash
curl -X DELETE http://localhost:5000/api/services/<SERVICE_ID>
```

---

## 6. Invoices API

### Get All Invoices
*Retrieve all saved bills, including calculated profit and expense for each.*
```bash
curl -X GET http://localhost:5000/api/invoices
```

### Get Single Invoice
*Retrieve detailed information for a specific bill.*
```bash
curl -X GET http://localhost:5000/api/invoices/<INVOICE_ID>
```

### Get Next Invoice Number
*Generate the next sequential invoice number.*
```bash
curl -X GET http://localhost:5000/api/invoices/next-number
```

### Get Analytics
*Get total bills, revenue, expense, and profit filtered by month/year. Only invoices with status "Completed" are included.*
```bash
curl -X GET "http://localhost:5000/api/invoices/analytics?month=1&year=2026"
```
**Response:**
```json
{
  "totalBills": 5,
  "totalRevenue": 5000.0,
  "totalExpense": 4000.0,
  "totalProfit": 1000.0
}
```

### Create Invoice
*Save a new bill. `invoiceNumber` is optional and will be auto-generated if omitted.*
```bash
curl -X POST http://localhost:5000/api/invoices \
  -H "Content-Type: application/json" \
  -d '{
    "invoiceNumber": "INV-001", (Optional)
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
    "paymentReceived": 1000.00,
    "status": "Enquiry", (Optional, defaults to Enquiry)
    "notes": "Thank you for your business",
    "lineItems": [
      {
        "productId": "<PRODUCT_ID>",
        "productName": "Hikvision 4MP IP Dome",
        "quantity": 2,
        "retailPrice": 3800.00,
        "gstPercentage": 18.0,
        "unit": "nos",
        "brandName": "Hikvision",
        "subCategoryId": "<SUBCATEGORY_ID>"
      },
      {
        "productName": "Installation Service",
        "quantity": 1,
        "retailPrice": 1500.00,
        "gstPercentage": 18.0,
        "isCustom": true
      }
    ]
  }'
```

### Update Invoice
*Modify an existing invoice (e.g., change status to "Completed" and record payment).*
```bash
curl -X PUT http://localhost:5000/api/invoices/<INVOICE_ID> \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Completed",
    "paymentReceived": 1200.00,
    "notes": "Payment received in full"
  }'
```

### Delete Invoice
*Cancel or remove an invoice.*
```bash
curl -X DELETE http://localhost:5000/api/invoices/<INVOICE_ID>
```

---

## 7. Company Details API

### Get Company Details
*Retrieve business details like bank info and GST number.*
```bash
curl -X GET http://localhost:5000/api/company
```

### Update Company Details
*Update the business profile displayed on invoices.*
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
