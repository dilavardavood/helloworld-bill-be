import requests
import json
import uuid

BASE_URL = "http://localhost:5000/api"

def get_analytics():
    res = requests.get(f"{BASE_URL}/invoices/analytics")
    res.raise_for_status()
    return res.json()

def test_status_and_analytics():
    print("🔍 Testing Invoice Status and Analytics Filtering...")
    
    # 1. Check initial analytics
    initial_analytics = get_analytics()
    print(f"Initial Analytics (Completed Bills): {initial_analytics['totalBills']}")

    # 2. Create an "Enquiry" invoice
    payload = {
        "invoiceNumber": f"STAT-{uuid.uuid4().hex[:4]}",
        "date": "2026-03-08T23:30:00",
        "customer": {"name": "Status Test Customer"},
        "lineItems": [
            {
                "productName": "Labor",
                "quantity": 1,
                "retailPrice": 500.0,
                "directPrice": 100.0,
                "isCustom": True
            }
        ],
        "subtotal": 500.0,
        "total": 590.0,
        "status": "Enquiry"
    }
    res = requests.post(f"{BASE_URL}/invoices", json=payload)
    res.raise_for_status()
    inv = res.json()
    print(f"✅ Created Enquiry Invoice: {inv['invoiceNumber']}")

    # 3. Check analytics again (should NOT increment)
    analytics_after_enquiry = get_analytics()
    if analytics_after_enquiry['totalBills'] != initial_analytics['totalBills']:
        raise Exception("Analytics incremented for Enquiry invoice!")
    print("✅ Analytics correctly ignored Enquiry invoice.")

    # 4. Update status to "Completed"
    update_payload = {
        "status": "Completed",
        "paymentReceived": 590.0
    }
    res = requests.put(f"{BASE_URL}/invoices/{inv['id']}", json=update_payload)
    res.raise_for_status()
    updated_inv = res.json()
    print(f"✅ Updated Invoice to Completed. Payment Received: {updated_inv['paymentReceived']}")

    # 5. Check analytics again (should increment)
    analytics_after_completed = get_analytics()
    if analytics_after_completed['totalBills'] != initial_analytics['totalBills'] + 1:
        raise Exception("Analytics did NOT increment after completing invoice!")
    print(f"✅ Analytics correctly included Completed invoice. Total Bills: {analytics_after_completed['totalBills']}")

if __name__ == "__main__":
    try:
        test_status_and_analytics()
        print("\n✅ Verification SUCCESS!")
    except Exception as e:
        print(f"\n❌ Verification FAILED: {str(e)}")
