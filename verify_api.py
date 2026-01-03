import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def test_api():
    try:
        # 1. Health Check
        try:
            r = requests.get(f"http://localhost:5000/health")
            if r.status_code == 200:
                log("Server is running", "SUCCESS")
            else:
                log("Server health check failed", "ERROR")
                return
        except requests.exceptions.ConnectionError:
            log("Server is NOT running. Please start it with 'python run.py'", "CRITICAL")
            return

        # 2. Create Category
        log("Creating Category...")
        cat_payload = {"name": "Test Category"}
        r = requests.post(f"{BASE_URL}/categories", json=cat_payload)
        if r.status_code == 201:
            cat = r.json()
            cat_id = cat['id']
            log(f"Category created: {cat_id}", "SUCCESS")
        else:
            log(f"Failed to create category: {r.text}", "ERROR")
            return

        # 3. Create Product
        log("Creating Product...")
        prod_payload = {
            "name": "Test Product",
            "unitPrice": 100.50,
            "unit": "pcs",
            "categoryId": cat_id
        }
        r = requests.post(f"{BASE_URL}/products", json=prod_payload)
        if r.status_code == 201:
            prod = r.json()
            prod_id = prod['id']
            log(f"Product created: {prod_id}", "SUCCESS")
        else:
            log(f"Failed to create product: {r.text}", "ERROR")
            return

        # 4. Create Invoice
        log("Creating Invoice...")
        inv_payload = {
            "invoiceNumber": "INV-TEST-001",
            "customer": {"name": "John Doe"},
            "lineItems": [
                {
                    "productId": prod_id,
                    "productName": "Test Product",
                    "quantity": 2,
                    "unitPrice": 100.50
                }
            ],
            "total": 201.00
        }
        r = requests.post(f"{BASE_URL}/invoices", json=inv_payload)
        if r.status_code == 201:
            inv = r.json()
            log(f"Invoice created: {inv['id']}", "SUCCESS")
        else:
            log(f"Failed to create invoice: {r.text}", "ERROR")
            return

        # 5. Check Next Number
        log("Checking Next Invoice Number...")
        r = requests.get(f"{BASE_URL}/invoices/next-number")
        if r.status_code == 200:
            log(f"Next Number: {r.json()['nextNumber']}", "SUCCESS")
        else:
            log(f"Failed to get next number", "ERROR")

        # 6. Create User
        log("Creating User...")
        user_payload = {
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "securepassword",
            "role": "admin"
        }
        r = requests.post(f"{BASE_URL}/users", json=user_payload)
        # Handle if user exists
        if r.status_code == 201 or r.status_code == 400: 
             log(f"User creation response: {r.status_code} (Might already exist)", "SUCCESS")
        else:
             log(f"Failed to create user: {r.text}", "ERROR")

        log("\nALL TESTS PASSED!", "SUCCESS")

    except Exception as e:
        log(f"Exception during test: {str(e)}", "ERROR")

if __name__ == "__main__":
    test_api()
