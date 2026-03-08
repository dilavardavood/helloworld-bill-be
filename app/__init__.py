from flask import Flask
from config import config
from app.extensions import db, migrate, cors

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # Register blueprints 
    from app.modules.users.routes import users_bp
    app.register_blueprint(users_bp, url_prefix='/api/users')

    from app.modules.company.routes import company_bp
    app.register_blueprint(company_bp, url_prefix='/api/company')

    from app.modules.categories.routes import categories_bp
    app.register_blueprint(categories_bp, url_prefix='/api/categories')

    from app.modules.products.routes import products_bp
    app.register_blueprint(products_bp, url_prefix='/api/products')

    from app.modules.invoices.routes import invoices_bp
    app.register_blueprint(invoices_bp, url_prefix='/api/invoices')

    from app.modules.services.routes import services_bp
    app.register_blueprint(services_bp, url_prefix='/api/services')
    
    @app.route('/health')
    def health_check():
        return {'status': 'ok'}

    return app
