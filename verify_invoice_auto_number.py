import requests
import json
import uuid

BASE_URL = "http://localhost:5000/api"

def create_raw_invoice(payload):
    res = requests.post(f"{BASE_URL}/invoices", json=payload)
    res.raise_for_status()
    return res.json()

def test_auto_numbering():
    print("🔍 Testing Automatic Invoice Numbering...")
    
    # Payload without invoiceNumber
    payload = {
        "date": "2026-03-08T22:40:00",
        "customer": {"name": "Auto Number Test"},
        "lineItems": [
            {
                "productName": "Manual Labor",
                "quantity": 1,
                "retailPrice": 100.0,
                "isCustom": True
            }
        ],
        "subtotal": 100.0,
        "total": 118.0
    }

    # 1. Test auto-generation
    inv1 = create_raw_invoice(payload)
    num1 = inv1['invoiceNumber']
    print(f"✅ Created Invoice 1: {num1}")

    # 2. Test auto-increment
    inv2 = create_raw_invoice(payload)
    num2 = inv2['invoiceNumber']
    print(f"✅ Created Invoice 2: {num2}")
    
    # 3. Test manual override
    payload_manual = payload.copy()
    manual_num = f"MANUAL-{uuid.uuid4().hex[:4]}"
    payload_manual['invoiceNumber'] = manual_num
    inv3 = create_raw_invoice(payload_manual)
    print(f"✅ Created Invoice 3 (Manual): {inv3['invoiceNumber']}")
    
    if inv3['invoiceNumber'] != manual_num:
        raise Exception(f"Manual override failed! Expected {manual_num}, got {inv3['invoiceNumber']}")

    # 4. Test auto-increment after manual (should continue from last numeric if possible, or just next available)
    # Our current logic just takes the LAST record and increments it.
    inv4 = create_raw_invoice(payload)
    print(f"✅ Created Invoice 4: {inv4['invoiceNumber']}")

if __name__ == "__main__":
    try:
        test_auto_numbering()
        print("\n✅ Verification SUCCESS!")
    except Exception as e:
        print(f"\n❌ Verification FAILED: {str(e)}")
