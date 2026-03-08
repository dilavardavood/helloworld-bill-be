import requests
import json
import uuid

BASE_URL = "http://localhost:5000/api"

def log(msg, status="INFO"):
    print(f"[{status}] {msg}")

def verify():
    try:
        # 1. Create Category with sub_category and brand_name
        log("Creating Category...")
        cat_payload = {
            "name": "Electronics",
            "subCategory": "Smartphones",
            "brandName": "Apple"
        }
        r = requests.post(f"{BASE_URL}/categories", json=cat_payload)
        if r.status_code == 201:
            cat = r.json()
            cat_id = cat['id']
            log(f"Category created: {cat_id}", "SUCCESS")
            assert cat['subCategory'] == "Smartphones"
            assert cat['brandName'] == "Apple"
        else:
            log(f"Failed to create category: {r.text}", "ERROR")
            return

        # 2. Create Product with sub_category and brand_name
        log("Creating Product...")
        prod_payload = {
            "name": "iPhone 15",
            "retailPrice": 999.00,
            "unit": "pcs",
            "subCategory": "Smartphones",
            "brandName": "Apple",
            "categoryId": cat_id
        }
        r = requests.post(f"{BASE_URL}/products", json=prod_payload)
        if r.status_code == 201:
            prod = r.json()
            prod_id = prod['id']
            log(f"Product created: {prod_id}", "SUCCESS")
            assert prod['subCategory'] == "Smartphones"
            assert prod['brandName'] == "Apple"
        else:
            log(f"Failed to create product: {r.text}", "ERROR")
            return

        # 3. Create Invoice and verify line item
        log("Creating Invoice...")
        inv_number = f"INV-{uuid.uuid4().hex[:6].upper()}"
        inv_payload = {
            "invoiceNumber": inv_number,
            "lineItems": [
                {
                    "productId": prod_id,
                    "productName": "iPhone 15",
                    "quantity": 1,
                    "retailPrice": 999.00
                }
            ]
        }
        r = requests.post(f"{BASE_URL}/invoices", json=inv_payload)
        if r.status_code == 201:
            inv = r.json()
            log(f"Invoice created: {inv['id']}", "SUCCESS")
            line_item = inv['lineItems'][0]
            log(f"Line Item: {line_item}", "INFO")
            assert line_item['subCategory'] == "Smartphones"
            assert line_item['brandName'] == "Apple"
            log("Line item preserved sub-category and brand name.", "SUCCESS")
        else:
            log(f"Failed to create invoice: {r.status_code} - {r.text}", "ERROR")
            return

        log("\nSUB-CATEGORY AND BRAND VERIFICATION PASSED!", "SUCCESS")

    except Exception as e:
        log(f"Exception during verification: {str(e)}", "ERROR")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verify()
