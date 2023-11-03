from flask import Flask
from .config import Config
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)

    # Initialize routes
    from .controllers import company_routes, material_routes, environmental_routes, industrial_routes, general_categories_routes
    app.register_blueprint(company_routes.company_bp)
    app.register_blueprint(material_routes.material_bp)
    app.register_blueprint(environmental_routes.environmental_bp)
    app.register_blueprint(industrial_routes.industrial_bp)
    app.register_blueprint(general_categories_routes.general_categories_bp)

    return app
