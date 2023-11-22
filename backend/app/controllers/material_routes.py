from flask import Blueprint, jsonify, abort, request
from app import db
from app.models.material_model import Material 
from app.models.general_categories_model import GeneralCategory
from app.services.material_service import get_all_materials, get_material_by_id
import logging
from sqlalchemy import exc, text

logger = logging.getLogger(__name__)

material_bp = Blueprint("material", __name__, url_prefix="/api/material")

@material_bp.route("/", methods=["GET"])
def get_materials():
    try:
        materials = get_all_materials()
        return jsonify(materials), 200
    except Exception as e:
        db.session.rollback()
        logger.exception("Failed to get materials") 
        abort(500, description="Internal Server Error")

@material_bp.route("/<int:material_id>", methods=["GET"])
def get_material(material_id):
    try:
        material = get_material_by_id(material_id)
        if material:
            return jsonify(material), 200
        else:
            abort(404, description="Material Not Found")
    except Exception as e:
        db.session.rollback()
        logger.exception(f"Failed to get material with ID {material_id}") 
        abort(500, description="Internal Server Error")

@material_bp.route('/add', methods=['POST'])
def add_material():
    from flask import request
    data = request.get_json()

    logger.info("Received material data: %s", data)

    if not validate_material_data(data):
        return jsonify({"error": "Invalid data"}), 400

    logger.info("Validated material data: %s", data)

    new_material = Material(
        materialname=data.get('materialName'),
        elementalcomposition=data.get('elementalComposition'),
        molecularweight=data.get('molecularWeight'),
        tensilestrength=data.get('tensileStrength'),
        ductility=data.get('ductility'),
        hardness=data.get('hardness'),
        thermalconductivity=data.get('thermalConductivity'),
        heatcapacity=data.get('heatCapacity'),
        meltingpoint=data.get('meltingPoint'),
        refractiveindex=data.get('refractiveIndex'),
        absorbance=data.get('absorbance'),
        conductivity=data.get('conductivity'),
        resistivity=data.get('resistivity'),
        generalcategoryid=data.get('generalCategoryID')
    )

    try:
        db.session.add(new_material)
        db.session.commit()
        return jsonify(new_material.to_dict()), 201
    except exc.IntegrityError:
        db.session.rollback()
        if 'material_pkey' in str(e.orig):
            logger.error("The 'materialid' is causing a unique constraint violation.")
        else:
            logger.error("Integrity error: %s", str(e))
        return jsonify({"error": "An integrity error occurred"}), 400
    except Exception as e:
        db.session.rollback()
        logger.exception("Unexpected error on adding new material")
        return jsonify({"error": str(e)}), 500

def validate_material_data(data):
    numeric_fields = [
        'molecularWeight', 'tensileStrength', 'ductility', 'hardness',
        'thermalConductivity', 'heatCapacity', 'meltingPoint', 'refractiveIndex',
        'conductivity', 'resistivity'
    ]

    for field in numeric_fields:
        if field in data and (data[field] is None or data[field] <= 0):
            return False

    if 'ductility' in data and not (0 <= data['ductility'] <= 2000):
        return False
    if 'absorbance' in data and not (0 <= data['absorbance'] <= 1):
        return False

    if 'materialName' in data and not data['materialName'].strip():
        return False
    if 'elementalComposition' in data and not data['elementalComposition'].strip():
        return False

    if 'generalCategoryID' in data:
        try:
            general_category_id = int(data['generalCategoryID'])
            if general_category_id <= 0:
                return False
            if not GeneralCategory.query.get(general_category_id):
                return False
        except (ValueError, TypeError):
            return False

    return True