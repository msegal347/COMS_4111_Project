from flask import Flask
from .config import Config
from .extensions import db, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions with the app
    db.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*", "methods": ["GET", "POST", "OPTIONS"]}}, headers=Config.CORS_HEADERS)

    # Register blueprints
    from .controllers import main
    app.register_blueprint(main)

    # Register other blueprints
    from .controllers import company_routes, material_routes, environmental_routes, industrial_routes, general_categories_routes, sold_by_routes, query_routes, execute_query_routes
    app.register_blueprint(company_routes.company_bp)
    app.register_blueprint(material_routes.material_bp)
    app.register_blueprint(environmental_routes.environmental_bp)
    app.register_blueprint(industrial_routes.industrial_bp)
    app.register_blueprint(general_categories_routes.general_categories_bp)
    app.register_blueprint(sold_by_routes.sold_by_bp)
    app.register_blueprint(query_routes.query_bp)
    app.register_blueprint(execute_query_routes.execute_query_bp)

    return app
