from flask import Blueprint, jsonify, request
from sqlalchemy import text
from app.extensions import db
import logging
import traceback 

logger = logging.getLogger("execute_query")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

execute_query_bp = Blueprint('execute_query', __name__, url_prefix='/api/execute-query')

QUERY_TEMPLATES = {
    'select_all_materials': 'SELECT * FROM Material',

    'select_all_companies': 'SELECT * FROM Company',

    'select_all_general_categories': '''
        SELECT * FROM GeneralCategories
    ''',

    'select_all_industrial_applications': '''
        SELECT ApplicationName, Industry, MaterialID
        FROM IndustrialApplications
    ''',

    'select_all_environmental_impacts': '''
        SELECT CarbonFootprint, MaterialID, ToxicityLevel
        FROM environmentalimpact
    ''',

    'select_all_materials_by_company_3M': '''
        SELECT Material.*
        FROM Material
        JOIN SoldBy
        ON Material.MaterialID = SoldBy.MaterialID
        JOIN Company
        ON SoldBy.CompanyID = Company.CompanyID
        WHERE Company.CompanyName = '3M'
    ''',
    
    'select_all_materials_metals': '''
        SELECT Material.*
        FROM Material
        JOIN GeneralCategories
        ON Material.GeneralCategoryID = GeneralCategories.GeneralCategoryID
        WHERE GeneralCategories.CategoryName = 'Metals'
    ''',

    'list_all_materials_with_applications_and_industries': '''
        SELECT 
            Material.MaterialName,
            IndustrialApplications.Industry,
            IndustrialApplications.ApplicationName
        FROM 
            Material
        LEFT JOIN 
            IndustrialApplications
        ON 
            Material.MaterialID = IndustrialApplications.MaterialID
    ''',

    'list_materials_sold_by_all_companies': '''
        SELECT
            Material.MaterialName,
            Company.CompanyName,
            SoldBy.BasePrice,
            SoldBy.Currency
        FROM
            Material
        INNER JOIN SoldBy ON Material.MaterialID = SoldBy.MaterialID
        INNER JOIN Company ON SoldBy.CompanyID = Company.CompanyID;
    ''',

    'list_materials_used_in_manufacturing_by_BASF': '''
        SELECT
            Material.MaterialName,
            Company.CompanyName,
            SoldBy.BasePrice,
            SoldBy.Currency,
            IndustrialApplications.ApplicationName
        FROM
            Material
        INNER JOIN SoldBy
            ON Material.MaterialID = SoldBy.MaterialID
        INNER JOIN Company
            ON SoldBy.CompanyID = Company.CompanyID
        INNER JOIN HasPracticalUses
            ON Material.MaterialID = HasPracticalUses.MaterialID
        INNER JOIN IndustrialApplications
            ON HasPracticalUses.ApplicationID = IndustrialApplications.ApplicationID
        WHERE
            Company.CompanyName = 'BASF'
            AND IndustrialApplications.ApplicationName = 'Cutting Tools Manufacturing';
    ''',

    'list_toxic_materials_sold_by_international_paper': '''
        SELECT 
            Material.MaterialName,
            EnvironmentalImpact.ToxicityLevel
        FROM 
            Material
        JOIN 
            SoldBy ON Material.MaterialID = SoldBy.MaterialID
        JOIN 
            Company ON SoldBy.CompanyID = Company.CompanyID
        JOIN 
            EnvironmentalImpact ON Material.MaterialID = EnvironmentalImpact.MaterialID
        WHERE 
            Company.CompanyName = 'International Paper'
        AND 
            EnvironmentalImpact.ToxicityLevel > 0;
    ''',

    'price_of_toxic_materials_with_tensile_strength_greater_than_100': '''
        SELECT DISTINCT
            Material.MaterialName,
            SoldBy.BasePrice,
            Material.TensileStrength,
            EnvironmentalImpact.ToxicityLevel
        FROM 
            Material
        INNER JOIN 
            EnvironmentalImpact ON Material.MaterialID = EnvironmentalImpact.MaterialID
        INNER JOIN 
            SoldBy ON Material.MaterialID = SoldBy.MaterialID
        WHERE 
            Material.TensileStrength > 100
        AND 
            EnvironmentalImpact.ToxicityLevel > 1;
    ''',

    'list_materials_with_average_price': '''
        SELECT 
            Material.MaterialName,
            AVG(SoldBy.BasePrice) AS AveragePrice
        FROM 
            Material
        JOIN 
            SoldBy ON Material.MaterialID = SoldBy.MaterialID
        GROUP BY 
            Material.MaterialName;
    ''',

    'top_5_most_toxic_materials': '''
        SELECT 
            Material.MaterialName,
            EnvironmentalImpact.ToxicityLevel
        FROM 
            Material
        JOIN 
            EnvironmentalImpact ON Material.MaterialID = EnvironmentalImpact.MaterialID
        ORDER BY 
            EnvironmentalImpact.ToxicityLevel DESC
        LIMIT 5;
    ''',

    'materials_with_their_categories_and_number_of_industrial_applications': '''
        SELECT 
            Material.MaterialName,
            GeneralCategories.CategoryName,
            COUNT(IndustrialApplications.ApplicationID) AS NumberOfApplications
        FROM 
            Material
        JOIN 
            GeneralCategories ON Material.GeneralCategoryID = GeneralCategories.GeneralCategoryID
        LEFT JOIN 
            IndustrialApplications ON Material.MaterialID = IndustrialApplications.MaterialID
        GROUP BY 
            Material.MaterialName, GeneralCategories.CategoryName;
    ''',

    'companies_and_count_of_materials_they_sell': '''
        SELECT 
            Company.CompanyName,
            COUNT(SoldBy.MaterialID) AS MaterialsCount
        FROM 
            Company
        JOIN 
            SoldBy ON Company.CompanyID = SoldBy.CompanyID
        GROUP BY 
            Company.CompanyName;
    ''',

    'materials_not_sold_by_any_company': '''
        SELECT 
            Material.MaterialName
        FROM 
            Material
        LEFT JOIN 
            SoldBy ON Material.MaterialID = SoldBy.MaterialID
        WHERE 
            SoldBy.CompanyID IS NULL;
    ''',

    'materials_with_high_carbon_footprint_and_environmental_impact': '''
        SELECT 
            Material.MaterialName,
            EnvironmentalImpact.CarbonFootprint,
            EnvironmentalImpact.ToxicityLevel
        FROM 
            Material
        JOIN 
            EnvironmentalImpact ON Material.MaterialID = EnvironmentalImpact.MaterialID
        WHERE 
            EnvironmentalImpact.CarbonFootprint > 5;
    ''',

    'materials_more_expensive_than_average_category_price': '''
        SELECT 
            M.MaterialName,
            GC.CategoryName,
            S.BasePrice,
            C.AvgCategoryPrice
        FROM 
            Material M
        JOIN 
            GeneralCategories GC ON M.GeneralCategoryID = GC.GeneralCategoryID
        JOIN 
            SoldBy S ON M.MaterialID = S.MaterialID
        JOIN (
            SELECT 
                Material.GeneralCategoryID,
                AVG(SoldBy.BasePrice) AS AvgCategoryPrice
            FROM 
                SoldBy
            JOIN Material ON SoldBy.MaterialID = Material.MaterialID
            GROUP BY Material.GeneralCategoryID
        ) AS C ON M.GeneralCategoryID = C.GeneralCategoryID
        WHERE 
            S.BasePrice > C.AvgCategoryPrice;


    ''',

    'companies_and_materials_they_sell_in_electronics_industry': '''
        SELECT 
            Company.CompanyName,
            Material.MaterialName
        FROM 
            Company
        JOIN 
            SoldBy ON Company.CompanyID = SoldBy.CompanyID
        JOIN 
            Material ON SoldBy.MaterialID = Material.MaterialID
        JOIN 
            IndustrialApplications ON Material.MaterialID = IndustrialApplications.MaterialID
        WHERE 
            IndustrialApplications.Industry = 'Electronics'
        GROUP BY 
            Company.CompanyName, Material.MaterialName;
    ''',

    'three_most_expensive_general_categories': '''
        SELECT 
            GC.CategoryName,
            AVG(SB.BasePrice) AS AvgPrice
        FROM 
            GeneralCategories GC
        JOIN 
            Material M ON GC.GeneralCategoryID = M.GeneralCategoryID
        JOIN 
            SoldBy SB ON M.MaterialID = SB.MaterialID
        GROUP BY 
            GC.CategoryName
        ORDER BY 
            AvgPrice DESC
        LIMIT 3;
    ''',
}


@execute_query_bp.route('', methods=['POST'])
def execute_query():
    data = request.get_json()
    query_key = data.get('query_key')
    parameters = data.get('parameters', {})

    logger.info(f"Received request for query_key: {query_key} with parameters: {parameters}")

    if query_key not in QUERY_TEMPLATES:
        logger.error("Query key not recognized")
        return jsonify({"error": "Query key not recognized"}), 400

    query_template = QUERY_TEMPLATES[query_key]
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text(query_template), parameters)
            rows = result.fetchall()
            result_list = [dict(row._mapping) for row in rows] 
            logger.info(f"Query executed successfully, returning {len(result_list)} rows")
            return jsonify(result_list), 200
    except Exception as e:
        logger.exception("Exception during query execution")
        error_trace = traceback.format_exc()
        return jsonify({"error": "Internal Server Error", "trace": error_trace}), 500


@execute_query_bp.before_request
def log_request():
    logger.debug(f"Handling request: {request.url} - {request.data}")


@execute_query_bp.after_request
def log_response(response):
    logger.debug(f"Response: {response.status} - {response.data}")
    return response
