import http.client
import json

def test_create_product():
    conn = http.client.HTTPConnection("localhost", 5000)
    headers = {'Content-Type': 'application/json'}
    payload = {
        "name": "Python Test Product",
        "retailPrice": 500.0,
        "unit": "pcs",
        "imageUrl": "http://example.com/api-image.jpg",
        "modelNumber": "MN-55",
        "serialNumber": "SN-99"
    }
    
    print(f"Sending request to localhost:5000/api/products...")
    conn.request("POST", "/api/products", json.dumps(payload), headers)
    
    response = conn.getresponse()
    print(f"Status: {response.status}")
    print(f"Reason: {response.reason}")
    data = response.read().decode()
    print(f"Response: {data}")
    conn.close()

if __name__ == "__main__":
    test_create_product()
