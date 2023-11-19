from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.orm import joinedload
from app.extensions import db
from app.models import Material, Company, EnvironmentalImpact, SoldBy, GeneralCategory, IndustrialApplication
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

        # Construct the base query
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
            IndustrialApplication,
            Material.materialid == IndustrialApplication.materialid
        )

        # Apply category filter
        category_filter = query_data.get('category')
        if category_filter:
            query = query.filter(GeneralCategory.categoryname == category_filter)

        # Apply company filter
        company_filter = query_data.get('company')
        if company_filter:
            query = query.filter(Company.companyname.ilike(f"%{company_filter}%"))

        # Apply industrial application filter
        application_filter = query_data.get('industrial')
        print(f"application_filter: {application_filter}")
        if application_filter:
            query = query.filter(IndustrialApplication.applicationname.ilike(f"%{application_filter}%"))

        # Debug: Print the query statement to check if it's correct
        print(query.statement.compile(compile_kwargs={"literal_binds": True}))

        # Execute the query
        results = query.distinct(Material.materialid)

        # Serialize results
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

        print(query)
        # Execute the query and fetch the results
        query_results = query.all()
        print(query_results)

        # Serialize results
        results = [{
            'material_id': material_instance.materialid,
            'material_name': material_instance.materialname,
            'category_id': material_instance.generalcategoryid,  # Add this line
            'category_name': category_name_instance,  # Assuming category_name is a string
            'elemental_composition': material_instance.elementalcomposition,
            'molecular_weight': material_instance.molecularweight,
            'tensile_strength': material_instance.tensilestrength,
            'ductility': material_instance.ductility,
            'hardness': material_instance.hardness,
            'thermal_conductivity': material_instance.thermalconductivity,
            'heat_capacity': material_instance.heatcapacity,
            'melting_point': material_instance.meltingpoint,
            'refractive_index': material_instance.refractiveindex,
            'absorbance': material_instance.absorbance,
            'conductivity': material_instance.conductivity,
            'resistivity': material_instance.resistivity,
            'created_at': material_instance.createdat.isoformat() if material_instance.createdat else None,
            'updated_at': material_instance.updatedat.isoformat() if material_instance.updatedat else None
        } for material_instance, category_name_instance in query_results]

        return jsonify(results), 200
    except Exception as e:
        current_app.logger.error(f'Error fetching materials: {e}')
        return jsonify({'error': str(e)}), 500

@query_bp.route('/industrial_applications', methods=['GET'])
def get_industrial_applications():
    try:
        industry_filter = request.args.get('industry', type=str)

        query = db.session.query(IndustrialApplication)
        if industry_filter:
            query = query.filter(IndustrialApplication.industry.ilike(f'%{industry_filter}%'))

        applications = query.all()
        applications_data = [app.to_dict() for app in applications]

        return jsonify(applications_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500