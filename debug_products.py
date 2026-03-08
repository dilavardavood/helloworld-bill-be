from app import create_app
from app.models import Product

app = create_app('default')
with app.app_context():
    try:
        products = Product.query.all()
        print(f"Found {len(products)} products")
        for p in products:
            try:
                p.to_dict()
            except Exception as e:
                print(f"Error in product {p.id}: {str(e)}")
                print(f"Data: retail_price={p.retail_price}, direct_price={p.direct_price}, gst_percentage={p.gst_percentage}")
                raise e
        print("All products to_dict successful")
    except Exception as e:
        print(f"General Error: {str(e)}")
        import traceback
        traceback.print_exc()
