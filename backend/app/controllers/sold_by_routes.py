from flask import Blueprint, jsonify, request, abort
from app import db
from app.models.sold_by_model import SoldBy
from app.services.sold_by_service import (
    get_all_sold_by_relations, get_sold_by_relation, create_sold_by_relation,
    update_sold_by_relation, delete_sold_by_relation
)
from app.models.material_model import Material
from app.models.company_model import Company
from sqlalchemy.exc import IntegrityError

sold_by_bp = Blueprint('sold_by', __name__, url_prefix='/api/sold_by')

# Helper function to validate the sold_by data
def validate_sold_by_data(data):
    required_fields = ['materialId', 'companyId', 'basePrice', 'currency']
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"{field} is required."

    try:
        base_price = float(data['basePrice'])
        if base_price < 0:
            return False, "basePrice must be a positive number."
    except ValueError:
        return False, "basePrice must be a number."

    if len(data['currency']) != 3:
        return False, "currency must be a 3-letter code."

    # Check if material and company exist
    try:
        material_id = int(data['materialId'])
    except (ValueError, TypeError):
        return False, "Material ID must be an integer."

    try:
        company_id = int(data['companyId'])
    except (ValueError, TypeError):
        return False, "Company ID must be an integer."

    if not Material.query.get(material_id):
        return False, "Material ID does not exist."
    
    if not Company.query.get(company_id):
        return False, "Company ID does not exist."

    return True, None

@sold_by_bp.route('/update', methods=['POST'])
def update_sold_by_entry():
    data = request.get_json()
    print(f"Received data: {data}")

    try:
        material = Material.query.filter_by(materialid=data.get('materialid')).first()
        company = Company.query.filter_by(companyid=data.get('companyid')).first()

        print(f"Found material: {material}")
        print(f"Found company: {company}")

        if not material or not company:
            return jsonify({'message': 'Material or Company not found'}), 404

        sold_by_entry = SoldBy.query.filter_by(materialid=material.materialid, companyid=company.companyid).first()
        print(f"Found or new sold_by_entry: {sold_by_entry}")

        if not sold_by_entry:
            # Provide the baseprice and currency when creating the SoldBy instance
            sold_by_entry = SoldBy(
                materialid=material.materialid,
                companyid=company.companyid,
                baseprice=data['basePrice'],
                currency=data['currency']
            )
            db.session.add(sold_by_entry)
        else:
            # If the entry exists, update the baseprice and currency
            sold_by_entry.baseprice = data['basePrice']
            sold_by_entry.currency = data['currency']

        db.session.commit()
        print(f"Committed sold_by_entry: {sold_by_entry}")

        return jsonify(sold_by_entry.to_dict()), 200
    except IntegrityError as e:
        db.session.rollback()
        print(f"IntegrityError: {e}")
        return jsonify({'message': 'IntegrityError: Unable to commit changes'}), 400
    except Exception as e:
        db.session.rollback()
        print(f"Exception: {e}")
        return jsonify({'message': str(e)}), 500


@sold_by_bp.route('/', methods=['GET'])
def get_relations():
    try:
        relations = get_all_sold_by_relations()
        return relations
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