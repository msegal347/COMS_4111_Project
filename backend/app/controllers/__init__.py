from flask import Blueprint

main = Blueprint('main', __name__)

# Import the modules that register blueprints
from . import company_routes
from . import environmental_routes
from . import general_categories_routes
from . import industrial_routes
from . import material_routes
from . import sold_by_routes

# Define the root route here if desired or you can leave it in the main app.py
@main.route('/')
def index():
    return 'Welcome to the Materials Database API!'
