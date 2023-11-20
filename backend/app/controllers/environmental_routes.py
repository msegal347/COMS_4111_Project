from flask import Blueprint, jsonify, request, abort
from app import db
from app.models.environmental_model import EnvironmentalImpact
from app.models.material_model import Material
import logging

logger = logging.getLogger('environmental_routes')

environmental_bp = Blueprint('environmental', __name__, url_prefix='/api/environmental')

@environmental_bp.route('/', methods=['GET'])
def get_environmental_impacts():
    try:
        impacts = EnvironmentalImpact.query.all()
        return jsonify([impact.to_dict() for impact in impacts]), 200
    except Exception as e:
        logger.error(f"Error fetching environmental impacts: {e}")
        abort(500, description="Internal Server Error")

@environmental_bp.route('/<int:impact_id>', methods=['GET'])
def get_environmental_impact(impact_id):
    try:
        impact = EnvironmentalImpact.query.get_or_404(impact_id)
        return jsonify(impact.to_dict()), 200
    except Exception as e:
        logger.error(f"Error fetching environmental impact with id {impact_id}: {e}")
        abort(500, description="Internal Server Error")
