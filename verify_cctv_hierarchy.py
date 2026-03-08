import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_categories():
    print("🔍 Testing Categories Hierarchy...")
    res = requests.get(f"{BASE_URL}/categories")
    res.raise_for_status()
    categories = res.json()
    print(f"Found {len(categories)} categories.")
    for cat in categories:
        print(f"Category: {cat['name']} (ID: {cat['id']})")
        for sub in cat.get('subCategories', []):
            print(f"  - SubCategory: {sub['name']} (ID: {sub['id']})")
    return categories

def test_products():
    print("\n🔍 Testing Products...")
    res = requests.get(f"{BASE_URL}/products")
    res.raise_for_status()
    products = res.json()
    print(f"Found {len(products)} products.")
    if products:
        p = products[0]
        print(f"Sample Product: {p['name']}")
        print(f"  Brand: {p['brandName']}")
        print(f"  SubCategory: {p['subCategoryName']}")
        print(f"  Category: {p['categoryName']}")
    return products

if __name__ == "__main__":
    try:
        test_categories()
        test_products()
        print("\n✅ Verification SUCCESS!")
    except Exception as e:
        print(f"\n❌ Verification FAILED: {str(e)}")
