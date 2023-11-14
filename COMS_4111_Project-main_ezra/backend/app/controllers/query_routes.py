from flask import Blueprint, request, jsonify, current_app
from app.extensions import db
from app.models import Material, Company, EnvironmentalImpact, SoldBy, GeneralCategory, IndustrialApplication
import traceback
import sys

query_bp = Blueprint('query', __name__, url_prefix='/api/query')


#query name is the name found in QueryPage.js (one of the beginning states)
def apply_filters(query, query_data, query_name, table_class,is_exact_match = False):
    if query_name in query_data:
            for key, value in query_data[query_name].items():
                if value:  # Only apply a filter if a value is provided
                    column = getattr(table_class, key.lower(), None)
                    if column is not None:
                        if is_exact_match:
                            query = query.filter(column == value)
                        else:
                            query = query.filter(column.ilike(f'%{value}%'))
    return query


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

    results_list = []

    try:
        query_data = request.get_json()

        #Querying from a few tables
        query = db.session.query(Material,GeneralCategory,Company,IndustrialApplication)
        # Join necessary tables based on filters provided
        if any(key in query_data for key in ['company', 'sold_by', 'environmental','category','industrialapplications']):
            query = query.join(SoldBy, Material.materialid == SoldBy.materialid) \
                        .join(Company, SoldBy.companyid == Company.companyid) \
                        .join(EnvironmentalImpact, Material.materialid == EnvironmentalImpact.materialid) \
                        .join(GeneralCategory, Material.generalcategoryid ==  GeneralCategory.generalcategoryid) \
                        .join(IndustrialApplication, Material.materialid ==  IndustrialApplication.materialid)
        query = apply_filters(query,query_data,'category',GeneralCategory)
        query = apply_filters(query,query_data,'material',Material)
        query = apply_filters(query,query_data,'company',Company,is_exact_match = True)
        query = apply_filters(query,query_data,'company_location',Company,is_exact_match = True)
        query = apply_filters(query,query_data,'industry',IndustrialApplication)
        query = apply_filters(query,query_data,'sold_by','SoldBy',is_exact_match = True)
        query = apply_filters(query,query_data,'environmental','EnvironmentalImpact',is_exact_match = True)

        # Execute the query
        results = query.all()

        # In your route, when preparing the results list:
        for material, generalcategory, company, industrial in results:
            material_dict = serialize_model(material)
            # Serialize the 'sold_by_relation' if it's a one-to-many relationship
            sold_by_list = serialize_model(material.sold_by_relation) if hasattr(material, 'sold_by_relation') else []
            environmental_dict = serialize_model(material.environmental_impact) if hasattr(material, 'environmental_impact') else {}
            categorical_dict = serialize_model(generalcategory)
            company_dict = serialize_model(company)
            industrial_dict = serialize_model(industrial)

            combined_result = {**material_dict, "sold_by": sold_by_list, **environmental_dict,**categorical_dict,**company_dict,**industrial_dict}
            #combined_result = {**material_dict,**categorical_dict,**company_dict}
            results_list.append(combined_result)
        print(results_list)
        
    except Exception as e:
        error_details = traceback.format_exc()
        current_app.logger.error(f'Error during query: {e}\nDetails: {error_details}')
        return jsonify({'error': str(e), 'details': error_details}), 500
    return jsonify(results_list), 200
