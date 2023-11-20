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
        SELECT ApplicationName, Industry
        FROM IndustrialApplications
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
        JOIN 
            HasPracticalUses ON Material.MaterialID = HasPracticalUses.MaterialID
        JOIN 
            IndustrialApplications ON HasPracticalUses.ApplicationID = IndustrialApplications.ApplicationID
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

    'list_materials_used_in_pharmaceuticals_by_BASF': '''
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
            AND IndustrialApplications.ApplicationName = 'Alloys and Pharmaceuticals';
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
            HasEffectOnEnvironment ON Material.MaterialID = HasEffectOnEnvironment.MaterialID
        JOIN 
            EnvironmentalImpact ON HasEffectOnEnvironment.ImpactID = EnvironmentalImpact.ImpactID
        WHERE 
            Company.CompanyName = 'International Paper'
        AND 
            EnvironmentalImpact.ToxicityLevel > 0
    ''',

    'price_of_toxic_materials_with_tensile_strength_greater_than_100': '''
        SELECT DISTINCT
            M.MaterialName,
            S.BasePrice,
            M.TensileStrength,
            EI.ToxicityLevel
        FROM 
            Material M
        INNER JOIN 
            HasEffectOnEnvironment HE ON M.MaterialID = HE.MaterialID
        INNER JOIN 
            EnvironmentalImpact EI ON HE.ImpactID = EI.ImpactID
        INNER JOIN 
            SoldBy S ON M.MaterialID = S.MaterialID
        WHERE 
            M.TensileStrength > 100
        AND 
            EI.ToxicityLevel > 1;
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
            M.MaterialName,
            EI.ToxicityLevel
        FROM 
            Material M
        JOIN 
            HasEffectOnEnvironment HE ON M.MaterialID = HE.MaterialID
        JOIN 
            EnvironmentalImpact EI ON HE.ImpactID = EI.ImpactID
        ORDER BY 
            EI.ToxicityLevel DESC
        LIMIT 5;
    ''',

    'materials_with_their_categories_and_number_of_industrial_applications': '''
        SELECT 
            M.MaterialName,
            GC.CategoryName,
            COUNT(HPU.ApplicationID) AS NumberOfApplications
        FROM 
            Material M
        JOIN 
            GeneralCategories GC ON M.GeneralCategoryID = GC.GeneralCategoryID
        LEFT JOIN 
            HasPracticalUses HPU ON M.MaterialID = HPU.MaterialID
        GROUP BY 
            M.MaterialName, GC.CategoryName;
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
            M.MaterialName,
            EI.CarbonFootprint,
            EI.ToxicityLevel
        FROM 
            Material M
        JOIN 
            HasEffectOnEnvironment HE ON M.MaterialID = HE.MaterialID
        JOIN 
            EnvironmentalImpact EI ON HE.ImpactID = EI.ImpactID
        WHERE 
            EI.CarbonFootprint > 5;
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
            C.CompanyName,
            M.MaterialName
        FROM 
            Company C
        JOIN 
            SoldBy S ON C.CompanyID = S.CompanyID
        JOIN 
            Material M ON S.MaterialID = M.MaterialID
        JOIN 
            HasPracticalUses HPU ON M.MaterialID = HPU.MaterialID
        JOIN 
            IndustrialApplications IA ON HPU.ApplicationID = IA.ApplicationID
        WHERE 
            IA.Industry = 'Electronics'
        GROUP BY 
            C.CompanyName, M.MaterialName;
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

    'all_materials_and_their_environmental_impacts': '''
        SELECT 
            m.MaterialName,
            e.ToxicityLevel,
            e.Recyclability,
            e.CarbonFootprint
        FROM 
            Material m
        JOIN 
            HasEffectOnEnvironment he ON m.MaterialID = he.MaterialID
        JOIN 
            EnvironmentalImpact e ON he.ImpactID = e.ImpactID;
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
            result_list = []
            for row in rows:
                row_dict = dict(row._mapping)
                for key, value in row_dict.items():
                    if isinstance(value, bool):
                        row_dict[key] = "TRUE" if value else "FALSE"
                result_list.append(row_dict)
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