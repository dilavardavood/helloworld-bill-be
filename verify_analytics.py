import requests
import json
import sys
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def test_analytics():
    try:
        # 1. Health Check
        r = requests.get(f"http://127.0.0.1:5000/health")
        if r.status_code != 200:
            log(f"Server is NOT running (Status: {r.status_code})", "CRITICAL")
            return

        # 2. Setup Category and Product
        log("Setting up data for analytics test...")
        cat_id = requests.post(f"{BASE_URL}/categories", json={"name": "Analytics Category"}).json()['id']
        
        prod_payload = {
            "name": "Profit Test Product",
            "retailPrice": 1000.00,
            "directPrice": 600.00,
            "gstPercentage": 10.0,
            "unit": "pcs",
            "categoryId": cat_id
        }
        prod_id = requests.post(f"{BASE_URL}/products", json=prod_payload).json()['id']

        # 3. Create Invoice
        # Profit should be: (Retail - Discount) - Direct
        # (1000 - 100) - 600 = 300
        log("Creating Invoice to test profit calculation...")
        inv_number = f"INV-ANL-{datetime.now().strftime('%M%S')}"
        inv_payload = {
            "invoiceNumber": inv_number,
            "date": datetime.now().isoformat(),
            "customer": {"name": "Analytics Customer"},
            "lineItems": [
                {
                    "productId": prod_id,
                    "productName": "Profit Test Product",
                    "quantity": 2,
                    "retailPrice": 1000.00,
                    "gstPercentage": 10.0,
                    "unit": "pcs"
                }
            ],
            "subtotal": 2000.00,
            "gstRate": 10.0,
            "gstAmount": 200.00,
            "discount": 200.00, # 10% discount on subtotal
            "total": 2000.00 # (2000 + 200) - 200 = 2000
        }
        # Expense = 2 * 600 = 1200
        # Revenue (Subtotal - Discount) = 2000 - 200 = 1800
        # Profit = 1800 - 1200 = 600
        
        r = requests.post(f"{BASE_URL}/invoices", json=inv_payload)
        if r.status_code != 201:
            log(f"Failed to create invoice: {r.text}", "ERROR")
            return
        inv = r.json()
        log(f"Invoice created: {inv['id']}", "SUCCESS")
        
        # 4. Verify Invoice Details
        log("Verifying calculated profit and expense in invoice response...")
        assert inv['calculatedExpense'] == 1200.0
        assert inv['calculatedProfit'] == 600.0
        log(f"Invoice Profit: {inv['calculatedProfit']}, Expense: {inv['calculatedExpense']}", "SUCCESS")

        # 5. Test Analytics API
        log("Testing Analytics API...")
        now = datetime.now()
        r = requests.get(f"{BASE_URL}/invoices/analytics?month={now.month}&year={now.year}")
        analytics = r.json()
        log(f"Analytics Data: {json.dumps(analytics, indent=2)}")
        
        assert analytics['totalBills'] >= 1
        assert analytics['totalProfit'] >= 600.0
        log("Analytics verification complete!", "SUCCESS")

        log("\nALL ANALYTICS TESTS PASSED!", "SUCCESS")

    except Exception as e:
        log(f"Exception during test: {str(e)}", "ERROR")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_analytics()
