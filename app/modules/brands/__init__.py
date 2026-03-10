from flask import Blueprint

brands_bp = Blueprint('brands', __name__)

from app.modules.brands import routes
