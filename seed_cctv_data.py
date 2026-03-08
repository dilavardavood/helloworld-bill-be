from app import create_app
from app.extensions import db
from app.models import Category, SubCategory, Product
import os

app = create_app(os.getenv('FLASK_ENV') or 'default')
with app.app_context():
    print("🌱 Seeding CCTV data...")
    try:
        # Define Data
        data = [
            {
                "category": "CCTV Cameras",
                "subcategories": [
                    {
                        "name": "HD Analog Dome",
                        "products": [
                            {"name": "Hikvision 2MP HD Dome", "price": 1450.0, "direct": 1100.0, "unit": "nos", "brand": "Hikvision"},
                            {"name": "CP Plus 2MP HD Dome", "price": 1250.0, "direct": 950.0, "unit": "nos", "brand": "CP Plus"}
                        ]
                    },
                    {
                        "name": "HD Analog Bullet",
                        "products": [
                            {"name": "Hikvision 2MP HD Bullet", "price": 1650.0, "direct": 1250.0, "unit": "nos", "brand": "Hikvision"},
                            {"name": "Dahua 2MP HD Bullet", "price": 1550.0, "direct": 1150.0, "unit": "nos", "brand": "Dahua"}
                        ]
                    },
                    {
                        "name": "IP Dome",
                        "products": [
                            {"name": "Hikvision 4MP IP Dome", "price": 3800.0, "direct": 2900.0, "unit": "nos", "brand": "Hikvision"},
                            {"name": "Dahua 4MP IP Dome", "price": 3600.0, "direct": 2750.0, "unit": "nos", "brand": "Dahua"}
                        ]
                    },
                    {
                        "name": "IP Bullet",
                        "products": [
                            {"name": "Hikvision 4MP IP Bullet", "price": 4200.0, "direct": 3200.0, "unit": "nos", "brand": "Hikvision"},
                            {"name": "CP Plus 4MP IP Bullet", "price": 3900.0, "direct": 3000.0, "unit": "nos", "brand": "CP Plus"}
                        ]
                    }
                ]
            },
            {
                "category": "Recording Devices",
                "subcategories": [
                    {
                        "name": "4CH DVR",
                        "products": [
                            {"name": "Hikvision 4CH Eco DVR", "price": 3200.0, "direct": 2500.0, "unit": "nos", "brand": "Hikvision"},
                            {"name": "Dahua 4CH Compact DVR", "price": 3000.0, "direct": 2350.0, "unit": "nos", "brand": "Dahua"}
                        ]
                    },
                    {
                        "name": "8CH DVR",
                        "products": [
                            {"name": "Hikvision 8CH Turbo DVR", "price": 5500.0, "direct": 4200.0, "unit": "nos", "brand": "Hikvision"},
                            {"name": "CP Plus 8CH HD DVR", "price": 5200.0, "direct": 4000.0, "unit": "nos", "brand": "CP Plus"}
                        ]
                    },
                    {
                        "name": "4CH NVR",
                        "products": [
                            {"name": "Hikvision 4CH POE NVR", "price": 6500.0, "direct": 5000.0, "unit": "nos", "brand": "Hikvision"}
                        ]
                    }
                ]
            },
            {
                "category": "Storage",
                "subcategories": [
                    {
                        "name": "Surveillance HDD",
                        "products": [
                            {"name": "Seagate SkyHawk 1TB", "price": 3800.0, "direct": 3100.0, "unit": "nos", "brand": "Seagate"},
                            {"name": "WD Purple 2TB", "price": 5800.0, "direct": 4800.0, "unit": "nos", "brand": "WD"}
                        ]
                    }
                ]
            },
            {
                "category": "Accessories",
                "subcategories": [
                    {
                        "name": "Power Supply",
                        "products": [
                            {"name": "ERD 5A Power Supply", "price": 450.0, "direct": 300.0, "unit": "nos", "brand": "ERD"},
                            {"name": "Consistent 10A PS", "price": 850.0, "direct": 600.0, "unit": "nos", "brand": "Consistent"}
                        ]
                    },
                    {
                        "name": "Cables",
                        "products": [
                            {"name": "3+1 CCTV Cable 90M", "price": 1800.0, "direct": 1400.0, "unit": "bundle", "brand": "D-Link"},
                            {"name": "CAT6 Ethernet Cable 305M", "price": 8500.0, "direct": 6500.0, "unit": "roll", "brand": "Digisol"}
                        ]
                    }
                ]
            }
        ]

        # Process Data
        for cat_data in data:
            cat = Category(name=cat_data["category"])
            db.session.add(cat)
            db.session.flush()
            
            for sub_data in cat_data["subcategories"]:
                sub = SubCategory(name=sub_data["name"], category_id=cat.id)
                db.session.add(sub)
                db.session.flush()
                
                for prod_data in sub_data["products"]:
                    prod = Product(
                        name=prod_data["name"],
                        retail_price=prod_data["price"],
                        direct_price=prod_data["direct"],
                        unit=prod_data["unit"],
                        brand_name=prod_data["brand"],
                        subcategory_id=sub.id,
                        gst_percentage=18.0
                    )
                    db.session.add(prod)
        
        db.session.commit()
        print("✨ CCTV data seeded successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding data: {str(e)}")
        import traceback
        traceback.print_exc()
