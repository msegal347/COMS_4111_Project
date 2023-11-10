from flask import Blueprint, jsonify, abort
from app import db
from app.services.material_service import get_all_materials, get_material_by_id
import logging

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
