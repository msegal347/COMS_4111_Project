from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.orm import joinedload
from app.extensions import db
from app.models import Material, Company, EnvironmentalImpact, SoldBy, GeneralCategory, IndustrialApplication, HasPracticalUses
import traceback

query_bp = Blueprint('query', __name__, url_prefix='/api/query')

def apply_filters(query, filter_data, table_class, is_exact_match=False):
    for key, value in filter_data.items():
        if value:
            column = getattr(table_class, key, None)
            if column:
                if is_exact_match:
                    query = query.filter(column == value)
                else:
                    query = query.filter(column.ilike(f'%{value}%'))
    return query

def serialize_model(model_instance):
    """Serialize a SQLAlchemy model instance into a dictionary."""
    return {column.name: getattr(model_instance, column.name) for column in model_instance.__table__.columns}

    

@query_bp.route('', methods=['POST'])
def run_query():
    try:
        query_data = request.get_json()
        current_app.logger.debug(f"Received query data: {query_data}")

        query = db.session.query(
            Material.materialname,
            GeneralCategory.categoryname,
            Company.companyname,
            IndustrialApplication.applicationname
        ).join(
            GeneralCategory,
            Material.generalcategoryid == GeneralCategory.generalcategoryid
        ).outerjoin(
            SoldBy,
            Material.materialid == SoldBy.materialid
        ).outerjoin(
            Company,
            SoldBy.companyid == Company.companyid
        ).outerjoin(
            HasPracticalUses,
            Material.materialid == HasPracticalUses.materialid
        ).outerjoin(
            IndustrialApplication,
            HasPracticalUses.applicationid == IndustrialApplication.applicationid
        )


        category_filter = query_data.get('category')
        if category_filter:
            query = query.filter(GeneralCategory.categoryname == category_filter)

        company_filter = query_data.get('company')
        if company_filter:
            query = query.filter(Company.companyname.ilike(f"%{company_filter}%"))

        application_filter = query_data.get('industrial')
        print(f"application_filter: {application_filter}")
        if application_filter:
            query = query.filter(IndustrialApplication.applicationname.ilike(f"%{application_filter}%"))

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        results = query.distinct(Material.materialid)

        results_list = [
            {
                'categoryname': result.categoryname,
                'materialname': result.materialname,
                'companyname': result.companyname or 'N/A',
                'applicationname': result.applicationname or 'N/A'
            }
            for result in results
        ]

        return jsonify(results_list), 200
    except Exception as e:
        error_details = traceback.format_exc()
        current_app.logger.error(f'Error during query execution: {e}\nDetails: {error_details}')
        return jsonify({'error': str(e), 'details': error_details}), 500

@query_bp.route('/materials', methods=['GET'])
def get_materials():
    try:
        category_name = request.args.get('category', type=str)
        query = db.session.query(
            Material,
            GeneralCategory.categoryname
        ).join(
            GeneralCategory,
            Material.generalcategoryid == GeneralCategory.generalcategoryid
        )
        
        if category_name:
            query = query.filter(GeneralCategory.categoryname == category_name)

        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        query_results = query.all()

        results = [serialize_model(material_instance) for material_instance, _ in query_results]
        results = [{"category_name": category_name_instance, **result} for result, category_name_instance in query_results]

        return jsonify(results), 200
    except Exception as e:
        current_app.logger.error(f'Error fetching materials: {e}')
        return jsonify({'error': str(e)}), 500

@query_bp.route('/industrial_applications', methods=['GET'])
def get_industrial_applications():
    try:
        industry_filter = request.args.get('industry', type=str)
        query = db.session.query(
            IndustrialApplication.applicationname,
            IndustrialApplication.industry,
            HasPracticalUses.materialid
        ).join(
            HasPracticalUses,
            HasPracticalUses.applicationid == IndustrialApplication.applicationid
        )

        if industry_filter:
            query = query.filter(IndustrialApplication.industry.ilike(f'%{industry_filter}%'))

        applications = query.all()
        applications_data = [{
            'application_name': app.applicationname,
            'industry': app.industry,
            'material_id': app.materialid
        } for app in applications]

        return jsonify(applications_data), 200
    except Exception as e:
        current_app.logger.error(f'Error fetching industrial applications: {e}')
        return jsonify({'error': str(e)}), 500