import requests
import json

BASE_URL = "http://localhost:5000/api/products"

def test_product_fields():
    print("--- Testing Product Fields ---")
    
    # 1. Create a product with new fields
    payload = {
        "name": "Test Product With Fields",
        "description": "A product to test new fields",
        "retailPrice": 100.0,
        "directPrice": 80.0,
        "gstPercentage": 18.0,
        "unit": "pcs",
        "imageUrl": "https://example.com/test-image.png",
        "modelNumber": "MOD-123",
        "serialNumber": "SER-456"
    }
    
    print(f"Creating product: {payload['name']}")
    response = requests.post(BASE_URL, json=payload)
    if response.status_code != 201:
        print(f"Failed to create product: {response.text}")
        return
    
    product = response.json()
    product_id = product['id']
    print(f"Product created with ID: {product_id}")
    
    # Verify fields in creation response
    assert product['imageUrl'] == payload['imageUrl']
    assert product['modelNumber'] == payload['modelNumber']
    assert product['serialNumber'] == payload['serialNumber']
    print("Fields verified in creation response.")
    
    # 2. Get the product and verify fields
    print(f"Fetching product: {product_id}")
    response = requests.get(BASE_URL)
    products = response.json()
    fetched_product = next((p for p in products if p['id'] == product_id), None)
    
    if not fetched_product:
        print("Product not found in list.")
        return
        
    assert fetched_product['imageUrl'] == payload['imageUrl']
    assert fetched_product['modelNumber'] == payload['modelNumber']
    assert fetched_product['serialNumber'] == payload['serialNumber']
    print("Fields verified in fetch response.")
    
    # 3. Update the fields
    update_payload = {
        "imageUrl": "https://example.com/updated-image.png",
        "modelNumber": "MOD-UPDATED",
        "serialNumber": "SER-UPDATED"
    }
    print(f"Updating product: {product_id}")
    response = requests.put(f"{BASE_URL}/{product_id}", json=update_payload)
    if response.status_code != 200:
        print(f"Failed to update product: {response.text}")
        return
        
    updated_product = response.json()
    assert updated_product['imageUrl'] == update_payload['imageUrl']
    assert updated_product['modelNumber'] == update_payload['modelNumber']
    assert updated_product['serialNumber'] == update_payload['serialNumber']
    print("Fields verified in update response.")
    
    # 4. Delete the product
    print(f"Deleting product: {product_id}")
    response = requests.delete(f"{BASE_URL}/{product_id}")
    if response.status_code == 204:
        print("Product deleted successfully.")
    else:
        print(f"Failed to delete product: {response.status_code}")

    print("--- All Tests Passed! ---")

if __name__ == "__main__":
    try:
        test_product_fields()
    except Exception as e:
        print(f"Test failed: {e}")
