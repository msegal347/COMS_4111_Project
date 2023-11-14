from flask import Blueprint, jsonify, request, abort
from app import db
from app.services.general_categories_service import (
    get_all_general_categories,
    get_general_category_by_id,
    create_general_category,
    update_general_category,
    delete_general_category,
)

general_categories_bp = Blueprint('general_categories', __name__, url_prefix='/api/general_categories')

@general_categories_bp.route('/', methods=['GET'])
def get_categories():
    try:
        categories = get_all_general_categories()
        return jsonify([category.to_dict() for category in categories]), 200
    except Exception as e:
        # Log the exception and return a 500 error
        abort(500, description=str(e))

@general_categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        category = get_general_category_by_id(category_id)
        if category:
            return jsonify(category.to_dict()), 200
        abort(404, description='Category not found')
    except Exception as e:
        abort(500, description=str(e))

@general_categories_bp.route('/', methods=['POST'])
def create_category():
    data = request.get_json()
    category_name = data.get('category_name')
    category = create_general_category(category_name)
    return jsonify(category.to_dict()), 201

@general_categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.get_json()
    category_name = data.get('category_name')
    category = update_general_category(category_id, category_name)
    if category:
        return jsonify(category.to_dict()), 200
    return jsonify({'message': 'Category not found'}), 404

@general_categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    success = delete_general_category(category_id)
    if success:
        return jsonify({}), 204
    return jsonify({'message': 'Category not found'}), 404
