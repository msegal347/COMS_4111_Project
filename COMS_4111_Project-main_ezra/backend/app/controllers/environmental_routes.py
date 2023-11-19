from flask import Blueprint, jsonify, request, abort
from app import db
from app.models.environmental_model import EnvironmentalImpact
import logging
from app.services.environmental_service import get_all_environmental_impacts

# Set up logger
logger = logging.getLogger('environmental_routes')

# Blueprint configuration
environmental_bp = Blueprint('environmental', __name__, url_prefix='/api/environmental')

# Helper function to serialize EnvironmentalImpact objects
def serialize_impact(impact):
    return {
        'impact_id': impact.impactid, 
        'material_id': impact.materialid,  
        'toxicity_level': impact.toxicitylevel, 
        'recyclability': impact.recyclability, 
        'carbon_footprint': impact.carbonfootprint
    }

@environmental_bp.route('/', methods=['GET'])
def get_environmental_impacts():
    try:
        impacts = get_all_environmental_impacts()
        #impacts = EnvironmentalImpact.query.all()
        #return jsonify([serialize_impact(impact) for impact in impacts]), 200
        return impacts
    except Exception as e:
        logger.error(f"Error fetching environmental impacts: {e}, Exception type: {type(e).__name__}")
        abort(500, description="Internal Server Error")

@environmental_bp.route('/<int:impact_id>', methods=['GET'])
def get_environmental_impact(impact_id):
    try:
        impact = EnvironmentalImpact.query.get_or_404(impact_id)
        return jsonify(serialize_impact(impact)), 200
    except Exception as e:
        logger.error(f"Error fetching environmental impact with id {impact_id}: {e}")
        abort(500, description="Internal Server Error")

