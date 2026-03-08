import requests
import json

BASE_URL = "http://localhost:5000/api"

def verify_fix():
    print("🔍 Verifying fix for get_invoices...")
    try:
        res = requests.get(f"{BASE_URL}/invoices")
        if res.status_code == 200:
            print("✅ get_invoices returned 200 OK")
            invoices = res.json()
            if invoices:
                last_inv = invoices[-1]
                print(f"Sample Invoice Status: {last_inv.get('status')}")
                print(f"Sample Invoice Payment Received: {last_inv.get('paymentReceived')}")
            else:
                print("ℹ️ No invoices found to check.")
            print("\n✅ API is working correctly!")
        else:
            print(f"❌ get_invoices returned {res.status_code}")
            print(res.text)
    except Exception as e:
        print(f"❌ Error during verification: {str(e)}")

if __name__ == "__main__":
    verify_fix()
