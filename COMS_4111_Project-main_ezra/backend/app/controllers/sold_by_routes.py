from flask import Blueprint, jsonify, request, abort
from app import db
from app.models.sold_by_model import SoldBy
from app.services.sold_by_service import (
    get_all_sold_by_relations, get_sold_by_relation, create_sold_by_relation,
    update_sold_by_relation, delete_sold_by_relation
)

sold_by_bp = Blueprint('sold_by', __name__, url_prefix='/api/sold_by')

@sold_by_bp.route('/', methods=['GET'])
def get_relations():
    try:
        relations = get_all_sold_by_relations()
        print([relation.to_dict() for relation in relations])
        return jsonify([relation.to_dict() for relation in relations]), 200
    except Exception as e:
        abort(500, description=str(e))

@sold_by_bp.route('/<int:material_id>/<int:company_id>', methods=['GET'])
def get_relation(material_id, company_id):
    try:
        relation = get_sold_by_relation(material_id, company_id)
        if relation:
            return jsonify(relation.to_dict()), 200
        else:
            abort(404, description="Sold by relation not found")
    except Exception as e:
        abort(500, description=str(e))

@sold_by_bp.route('/', methods=['POST'])
def create_relation():
    data = request.get_json()
    try:
        new_relation = create_sold_by_relation(data)
        return jsonify(new_relation.to_dict()), 201
    except Exception as e:
        abort(500, description=str(e))

@sold_by_bp.route('/<int:material_id>/<int:company_id>', methods=['PUT'])
def update_relation(material_id, company_id):
    data = request.get_json()
    try:
        updated_relation = update_sold_by_relation(material_id, company_id, data)
        if updated_relation:
            return jsonify(updated_relation.to_dict()), 200
        else:
            abort(404, description="Sold by relation not found")
    except Exception as e:
        abort(500, description=str(e))

@sold_by_bp.route('/<int:material_id>/<int:company_id>', methods=['DELETE'])
def delete_relation(material_id, company_id):
    try:
        delete_sold_by_relation(material_id, company_id)
        return '', 204
    except Exception as e:
        abort(500, description=str(e))
