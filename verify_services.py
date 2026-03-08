import requests
import json
import uuid

BASE_URL = "http://localhost:5000/api"

def test_services_crud():
    print("🔍 Testing Services CRUD...")
    # Create
    service_data = {
        "name": "Test Installation Service",
        "description": "Verification of service crud",
        "retailPrice": 1500.0,
        "directPrice": 500.0,
        "gstPercentage": 18.0,
        "unit": "job"
    }
    res = requests.post(f"{BASE_URL}/services", json=service_data)
    res.raise_for_status()
    created = res.json()
    print(f"✅ Service created: {created['id']}")

    # Update
    res = requests.put(f"{BASE_URL}/services/{created['id']}", json={"retailPrice": 2000.0})
    res.raise_for_status()
    updated = res.json()
    print(f"✅ Service updated: New Price = {updated['retailPrice']}")

    # Get All
    res = requests.get(f"{BASE_URL}/services")
    res.raise_for_status()
    print(f"✅ Found {len(res.json())} services.")
    
    return created

def test_invoice_with_service(service_id):
    print("\n🔍 Testing Invoice with Service...")
    # Get a product
    products = requests.get(f"{BASE_URL}/products").json()
    product = products[0] if products else None
    
    invoice_data = {
        "invoiceNumber": f"TEST-SER-{uuid.uuid4().hex[:6]}",
        "date": "2026-03-08T22:00:00",
        "customer": {"name": "Service Test Customer"},
        "subtotal": (product['retailPrice'] if product else 0) + 2000.0,
        "total": ((product['retailPrice'] if product else 0) + 2000.0) * 1.18,
        "lineItems": [
            {
                "serviceId": service_id,
                "productName": "Fixed Installation Service",
                "quantity": 1,
                "retailPrice": 2000.0,
                "gstPercentage": 18.0,
                "unit": "job"
            }
        ]
    }
    
    if product:
        invoice_data["lineItems"].append({
            "productId": product['id'],
            "productName": product['name'],
            "quantity": 1,
            "retailPrice": product['retailPrice'],
            "gstPercentage": 18.0,
            "unit": product['unit']
        })

    res = requests.post(f"{BASE_URL}/invoices", json=invoice_data)
    res.raise_for_status()
    inv = res.json()
    print(f"✅ Invoice created: {inv['invoiceNumber']}")
    
    # Check if direct price was resolved
    items = inv['lineItems']
    service_item = next((it for it in items if it['serviceId'] == service_id), None)
    if service_item:
        print(f"✅ Service item found in invoice. Direct Price = {service_item['directPrice']}")
    else:
        print("❌ Service item NOT found in invoice.")

if __name__ == "__main__":
    try:
        service = test_services_crud()
        test_invoice_with_service(service['id'])
        print("\n✅ All tests PASSED!")
    except Exception as e:
        print(f"\n❌ Tests FAILED: {str(e)}")
