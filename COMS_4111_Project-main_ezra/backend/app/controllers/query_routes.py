from flask import Blueprint, request, jsonify, current_app
from app.extensions import db
from app.models import Material, Company, EnvironmentalImpact, SoldBy, GeneralCategory
import traceback
import sys

query_bp = Blueprint('query', __name__, url_prefix='/api/query')

def serialize_model(model_instance):
    """Serialize a SQLAlchemy model instance or a list of instances."""
    if isinstance(model_instance, list):
        # Handle the list of instances
        return [serialize_model(item) for item in model_instance]
    else:
        # Handle a single instance
        return {column.name: getattr(model_instance, column.name) for column in model_instance.__table__.columns}


@query_bp.route('', methods=['POST'])
def run_query():
    print('Hello world!', file=sys.stderr)

    results_list = []

    try:
        query_data = request.get_json()

        # Start with a base query of Material
        query = db.session.query(Material,GeneralCategory)
        print(query_data, file=sys.stderr)
        # Join necessary tables based on filters provided
        if any(key in query_data for key in ['company', 'sold_by', 'environmental','category']):
            query = query.join(SoldBy, Material.materialid == SoldBy.materialid) \
                        .join(Company, SoldBy.companyid == Company.companyid) \
                        .join(EnvironmentalImpact, Material.materialid == EnvironmentalImpact.materialid) \
                        .join(GeneralCategory, Material.generalcategoryid ==  GeneralCategory.generalcategoryid)

        print(query, file=sys.stderr)
        # Apply filters for GeneralCategory
        if 'category' in query_data:
            print('Hello world 1.5!', file=sys.stderr)
            for key, value in query_data['category'].items():
                print('Hello world 2!', file=sys.stderr)
                if value:  # Only apply a filter if a value is provided
                    column = getattr(GeneralCategory, key.lower(), None)
                    if column is not None:
                        query = query.filter(column.ilike(f'%{value}%'))

        # Apply filters for Material
        if 'material' in query_data:
            print('Hello world 3!', file=sys.stderr)
            for key, value in query_data['material'].items():
                print('Hello world 4!', file=sys.stderr)
                if value:  # Only apply a filter if a value is provided
                    column = getattr(Material, key.lower(), None)
                    if column is not None:
                        query = query.filter(column.ilike(f'%{value}%'))

        # Apply filters for Company
        if 'company' in query_data:
            for key, value in query_data['company'].items():
                if value:  # Only apply a filter if a value is provided
                    column = getattr(Company, key.lower(), None)
                    if column is not None:
                        query = query.filter(column == value)

        # Apply filters for SoldBy (assuming you have flags like is_sold_by_company_a)
        if 'sold_by' in query_data:
            for key, value in query_data['sold_by'].items():
                if value:  # Only apply a filter if a flag is true
                    column = getattr(SoldBy, key.lower(), None)
                    if column is not None:
                        query = query.filter(column == value)

        # Apply filters for EnvironmentalImpact
        if 'environmental' in query_data:
            for key, value in query_data['environmental'].items():
                if value:  # Only apply a filter if a value is provided
                    column = getattr(EnvironmentalImpact, key.lower(), None)
                    if column is not None:
                        query = query.filter(column == value)

        # Execute the query
        results = query.all()
        print(results, file=sys.stderr)

        # In your route, when preparing the results list:
        for material,generalcategory in results:
            print(material, file=sys.stderr)
            material_dict = serialize_model(material)
            # Serialize the 'sold_by_relation' if it's a one-to-many relationship
            sold_by_list = serialize_model(material.sold_by_relation) if hasattr(material, 'sold_by_relation') else []
            environmental_dict = serialize_model(material.environmental_impact) if hasattr(material, 'environmental_impact') else {}
            categorical_dict = serialize_model(generalcategory)

            combined_result = {**material_dict, "sold_by": sold_by_list, **environmental_dict,**categorical_dict}
            results_list.append(combined_result)
        
    except Exception as e:
        error_details = traceback.format_exc()
        current_app.logger.error(f'Error during query: {e}\nDetails: {error_details}')
        return jsonify({'error': str(e), 'details': error_details}), 500
    print(results_list, file=sys.stderr)
    return jsonify(results_list), 200
