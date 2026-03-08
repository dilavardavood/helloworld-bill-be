import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def test_upgrade():
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
        log("Creating Category for upgrade test...")
        cat_payload = {"name": "Upgrade Test Category"}
        r = requests.post(f"{BASE_URL}/categories", json=cat_payload)
        cat_id = r.json()['id']
        log(f"Category created: {cat_id}", "SUCCESS")

        # 3. Create Product with new fields
        log("Creating Product with retailPrice, directPrice, and gstPercentage...")
        prod_payload = {
            "name": "Upgrade Test Product",
            "retailPrice": 1200.00,
            "directPrice": 900.00,
            "gstPercentage": 18.0,
            "unit": "pcs",
            "categoryId": cat_id
        }
        r = requests.post(f"{BASE_URL}/products", json=prod_payload)
        if r.status_code == 201:
            prod = r.json()
            prod_id = prod['id']
            log(f"Product created successfully: {prod_id}", "SUCCESS")
            log(f"Product Data: {json.dumps(prod, indent=2)}")
            
            # Verify fields
            assert prod['retailPrice'] == 1200.00
            assert prod['directPrice'] == 900.00
            assert prod['gstPercentage'] == 18.0
        else:
            log(f"Failed to create product: {r.text}", "ERROR")
            return

        # 4. Create Invoice with new fields in line items
        log("Creating Invoice with retailPrice and gstPercentage in line items...")
        inv_payload = {
            "invoiceNumber": f"INV-UPGR-{int(sys.float_info.max % 10000)}", # Randomish
            "date": "2026-01-13T10:00:00",
            "customer": {"name": "Upgrade Customer"},
            "lineItems": [
                {
                    "productId": prod_id,
                    "productName": "Upgrade Test Product",
                    "quantity": 1,
                    "retailPrice": 1200.00,
                    "gstPercentage": 18.0,
                    "unit": "pcs",
                    "categoryId": cat_id
                }
            ],
            "subtotal": 1200.00,
            "gstRate": 18.0,
            "gstAmount": 216.00,
            "total": 1416.00
        }
        r = requests.post(f"{BASE_URL}/invoices", json=inv_payload)
        if r.status_code == 201:
            inv = r.json()
            log(f"Invoice created successfully: {inv['id']}", "SUCCESS")
            log(f"Invoice Data: {json.dumps(inv, indent=2)}")
            
            # Verify line item fields
            item = inv['lineItems'][0]
            assert item['retailPrice'] == 1200.00
            assert item['gstPercentage'] == 18.0
        else:
            log(f"Failed to create invoice: {r.text}", "ERROR")
            return

        log("\nUPGRADE TESTS PASSED!", "SUCCESS")

    except Exception as e:
        log(f"Exception during test: {str(e)}", "ERROR")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_upgrade()
