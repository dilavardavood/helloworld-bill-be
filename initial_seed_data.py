import requests

BASE_URL = "http://localhost:5000/api"
HEADERS = {"Content-Type": "application/json"}

# -----------------------------
# Helper functions
# -----------------------------

def get_categories():
    res = requests.get(f"{BASE_URL}/categories")
    res.raise_for_status()
    return res.json()

def create_category(name):
    res = requests.post(
        f"{BASE_URL}/categories",
        json={"name": name},
        headers=HEADERS
    )
    res.raise_for_status()
    return res.json()

def get_products():
    res = requests.get(f"{BASE_URL}/products")
    res.raise_for_status()
    return res.json()

def create_product(product):
    res = requests.post(
        f"{BASE_URL}/products",
        json=product,
        headers=HEADERS
    )
    res.raise_for_status()
    return res.json()

# -----------------------------
# Seed Data
# -----------------------------

CATEGORIES = [
    "IP Camera",
    "HD Camera",
    "PTZ Camera",
    "DVR",
    "NVR",
    "Accessories",
    "Services"
]

PRODUCTS = {
    "IP Camera": [
        {
            "name": "IP Camera 5MP",
            "description": "5MP IP Camera with Night Vision",
            "unitPrice": 3500.00,
            "unit": "nos"
        },
        {
            "name": "IP Camera 8MP",
            "description": "8MP Ultra HD IP Camera",
            "unitPrice": 5500.00,
            "unit": "nos"
        }
    ],
    "HD Camera": [
        {
            "name": "HD Camera 5MP",
            "description": "5MP HD Camera Day & Night",
            "unitPrice": 2750.00,
            "unit": "nos"
        }
    ],
    "PTZ Camera": [
        {
            "name": "PTZ Camera 4MP",
            "description": "4MP PTZ Camera with Zoom",
            "unitPrice": 12000.00,
            "unit": "nos"
        }
    ],
    "DVR": [
        {
            "name": "DVR 4CH 5MP",
            "description": "4 Channel DVR supporting 5MP",
            "unitPrice": 4200.00,
            "unit": "nos"
        }
    ],
    "NVR": [
        {
            "name": "NVR 8CH",
            "description": "8 Channel NVR",
            "unitPrice": 6500.00,
            "unit": "nos"
        }
    ],
    "Accessories": [
        {
            "name": "500GB Hard Disk",
            "description": "Surveillance Grade HDD",
            "unitPrice": 2600.00,
            "unit": "nos"
        },
        {
            "name": "4CH Power Supply",
            "description": "Power Supply for 4 Cameras",
            "unitPrice": 550.00,
            "unit": "nos"
        }
    ],
    "Services": [
        {
            "name": "Installation Charges",
            "description": "Installation & Configuration",
            "unitPrice": 3000.00,
            "unit": "job"
        }
    ]
}

# -----------------------------
# Main Seeder Logic
# -----------------------------

def main():
    print("🔍 Checking existing categories...")
    existing_categories = get_categories()
    category_map = {c["name"]: c["id"] for c in existing_categories}

    # Create categories
    for cat in CATEGORIES:
        if cat not in category_map:
            print(f"➕ Creating category: {cat}")
            created = create_category(cat)
            category_map[cat] = created["id"]
        else:
            print(f"✔ Category exists: {cat}")

    print("\n🔍 Checking existing products...")
    existing_products = get_products()
    product_names = {p["name"] for p in existing_products}

    # Create products
    for category, items in PRODUCTS.items():
        category_id = category_map[category]

        for item in items:
            if item["name"] in product_names:
                print(f"✔ Product exists: {item['name']}")
                continue

            payload = {
                "name": item["name"],
                "description": item["description"],
                "unitPrice": item["unitPrice"],
                "unit": item["unit"],
                "categoryId": category_id
            }

            print(f"➕ Creating product: {item['name']}")
            create_product(payload)

    print("\n✅ Seeding completed successfully!")

# -----------------------------
# Run
# -----------------------------

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("❌ Error while seeding data:")
        print(e)
