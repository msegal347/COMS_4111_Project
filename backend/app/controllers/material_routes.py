from flask import Blueprint, jsonify, abort
from app.extensions import db
from app.models.material_model import Material
from app.services.material_service import get_all_materials, get_material_by_id
import logging

logger = logging.getLogger(__name__)

material_bp = Blueprint("material", __name__, url_prefix="/api/material")

@material_bp.route("/", methods=["GET"])
def get_materials():
    try:
        materials = get_all_materials()
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to get materials: {e}")
        abort(500, description="Internal Server Error")
    return jsonify(materials), 200

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
        abort(500, description="Internal Server Error")
