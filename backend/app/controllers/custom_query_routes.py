from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import text
from app.extensions import db
import logging
import traceback 


logger = logging.getLogger("custom_query")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

custom_query_bp = Blueprint('custom_query', __name__, url_prefix='/api/custom-query')


@custom_query_bp.route('', methods=['POST'])
def custom_query():
    logger.debug("Handling custom query request")
    try:
        # Corrected code to obtain a connection from the engine
        with current_app.app_context():
            connection = db.engine.connect()

            logger.debug("Fetching dropdown data for general categories")
            general_categories = connection.execute(text("SELECT CategoryName FROM GeneralCategories")).fetchall()

            logger.debug("Fetching dropdown data for companies")
            companies = connection.execute(text("SELECT CompanyName FROM Company")).fetchall()
        
            logger.debug("Fetching dropdown data for industrial applications")
            industrial_applications = connection.execute(text("SELECT ApplicationName FROM IndustrialApplications")).fetchall()

        logger.debug("Dropdown data fetched successfully")

        query_data = request.get_json()
        logger.debug(f"Received query data: {query_data}")

        dropdown_data = {
            "general_categories": [category[0] for category in general_categories],
            "companies": [company[0] for company in companies],
            "industrial_applications": [application[0] for application in industrial_applications]
        }

        query_data = request.get_json()
        category_filter = query_data.get('category')
        company_filter = query_data.get('company')
        application_filter = query_data.get('application')

        # Base SQL query
        query = """
        SELECT DISTINCT
            m.MaterialName,
            gc.CategoryName,
            c.CompanyName,
            ia.ApplicationName
        FROM Material m
        LEFT JOIN GeneralCategories gc ON m.GeneralCategoryID = gc.GeneralCategoryID
        LEFT JOIN SoldBy s ON m.MaterialID = s.MaterialID
        LEFT JOIN Company c ON s.CompanyID = c.CompanyID
        LEFT JOIN HasPracticalUses hpu ON m.MaterialID = hpu.MaterialID
        LEFT JOIN IndustrialApplications ia ON hpu.ApplicationID = ia.ApplicationID
        """

        # Adding conditions for filtering
        conditions = []
        params = {}
        if category_filter:
            conditions.append("gc.CategoryName = :category")
            params['category'] = category_filter
        if company_filter:
            conditions.append("c.CompanyName LIKE :company")
            params['company'] = f"%{company_filter}%"
        if application_filter:
            conditions.append("ia.ApplicationName LIKE :application")
            params['application'] = f"%{application_filter}%"

        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)

        with db.engine.connect() as connection:
            logger.debug("Executing custom query")
            result = connection.execute(text(query).params(**params))
            
            logger.debug("Query executed successfully")
            rows = [row._asdict() for row in result]
            logger.debug("rows: " + str(rows))
            
        logger.debug("Sending back query results")
        return jsonify({"dropdown_data": dropdown_data, "query_results": rows}), 200

    except Exception as e:
        logger.exception("Exception during query execution")
        return jsonify({"error": "Internal Server Error", "trace": traceback.format_exc()}), 500



