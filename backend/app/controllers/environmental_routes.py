from flask import Blueprint, jsonify, request, abort
from app import db 
from app.models.environmental_model import EnvironmentalImpact
import logging

# Set up logger
logger = logging.getLogger('environmental_routes')

# Blueprint configuration
environmental_bp = Blueprint('environmental', __name__, url_prefix='/api/environmental')

# Helper function to serialize EnvironmentalImpact objects
def serialize_impact(impact):
    return {
        'impact_id': impact.ImpactID,
        'material_id': impact.MaterialID,
        'toxicity_level': impact.ToxicityLevel,
        'recyclability': impact.Recyclability,
        'carbon_footprint': impact.CarbonFootprint
    }

@environmental_bp.route('/', methods=['GET'])
def get_environmental_impacts():
    try:
        impacts = EnvironmentalImpact.query.all()
        return jsonify([serialize_impact(impact) for impact in impacts]), 200
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

@environmental_bp.route('/', methods=['POST'])
def create_environmental_impact():
    data = request.get_json()
    try:
        new_impact = EnvironmentalImpact(**data)
        db.session.add(new_impact)
        db.session.commit()
        return jsonify(serialize_impact(new_impact)), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating new environmental impact: {e}")
        abort(500, description="Internal Server Error")

@environmental_bp.route('/<int:impact_id>', methods=['PUT'])
def update_environmental_impact(impact_id):
    data = request.get_json()
    try:
        impact = EnvironmentalImpact.query.get_or_404(impact_id)
        for key, value in data.items():
            setattr(impact, key, value)
        db.session.commit()
        return jsonify(serialize_impact(impact)), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating environmental impact with id {impact_id}: {e}")
        abort(500, description="Internal Server Error")

@environmental_bp.route('/<int:impact_id>', methods=['DELETE'])
def delete_environmental_impact(impact_id):
    try:
        impact = EnvironmentalImpact.query.get_or_404(impact_id)
        db.session.delete(impact)
        db.session.commit()
        return jsonify({}), 204
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting environmental impact with id {impact_id}: {e}")
        abort(500, description="Internal Server Error")
