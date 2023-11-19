from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import text
from app.extensions import db
import logging

# Set up logger for this module
logger = logging.getLogger("execute_query")
logger.setLevel(logging.INFO)  # Set to DEBUG if you want all messages
handler = logging.StreamHandler()  # Set up the handler to print to the console
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Create a Blueprint for the execute-query route
execute_query_bp = Blueprint('execute_query', __name__, url_prefix='/api/execute-query')

# Predefined safe queries with placeholders
# Predefined safe queries with placeholders
QUERY_TEMPLATES = {
    'select_materials_by_category': 'SELECT * FROM Material WHERE GeneralCategoryID = (SELECT GeneralCategoryID FROM GeneralCategories WHERE CategoryName = :category)'
}


@execute_query_bp.route('', methods=['POST'])
def execute_query():
    data = request.get_json()
    query_key = data.get('query_key')
    parameters = data.get('parameters', {})

    if query_key not in QUERY_TEMPLATES:
        return jsonify({"error": "Query key not recognized"}), 400

    query_template = QUERY_TEMPLATES[query_key]

    try:
        # Explicitly pushing an application context
        with current_app.app_context():
            # Now you can safely call db.engine
            engine = db.get_engine()
            with engine.connect() as connection:
                result = connection.execute(text(query_template), **parameters)
                rows = [dict(row) for row in result]
                return jsonify(rows), 200
    except Exception as e:
        current_app.logger.error(f'Error during query execution: {e}')
        return jsonify({'error': str(e)}), 500

# If you want to log every request to the blueprint, you can use before_request
@execute_query_bp.before_request
def before_request():
    logger.debug(f"Handling request: {request.url} - {request.data}")

# Similarly, if you want to log responses:
@execute_query_bp.after_request
def after_request(response):
    logger.debug(f"Response: {response.status} - {response.data}")
    return response