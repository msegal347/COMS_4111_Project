from app.extensions import db
from app.models.environmental_model import EnvironmentalImpact
from app.models.material_model import Material
import logging

# Set up logger
logger = logging.getLogger('environmental_service')

def get_all_environmental_impacts():
    """
    Retrieves all environmental impacts from the database.
    Returns:
        List[EnvironmentalImpact]: A list of EnvironmentalImpact model instances.
    """
    try:
        environmental_query = db.session.query(EnvironmentalImpact,Material.materialname).join(
        Material,
        EnvironmentalImpact.materialid == Material.materialid).all()
        return [
        {
            "impact_id": environmental.EnvironmentalImpact.impactid,
            "material_name": environmental.materialname,
            "toxicity_level": environmental.EnvironmentalImpact.toxicitylevel,
            "recyclability": environmental.EnvironmentalImpact.recyclability,
            "carbon_footprint": environmental.EnvironmentalImpact.carbonfootprint,
        }
        for environmental in environmental_query
    ]
    except Exception as e:
        logger.error(f"Error retrieving all environmental impacts: {e}")
        raise

def get_environmental_impact_by_id(impact_id):
    """
    Retrieves an environmental impact by its ID.
    Args:
        impact_id (int): The ID of the environmental impact to retrieve.
    Returns:
        EnvironmentalImpact: An instance of EnvironmentalImpact if found, otherwise None.
    """
    try:
        return EnvironmentalImpact.query.get(impact_id)
    except Exception as e:
        logger.error(f"Error retrieving environmental impact with ID {impact_id}: {e}")
        raise

def create_environmental_impact(data):
    """
    Creates a new environmental impact record in the database.
    Args:
        data (dict): A dictionary with the required fields to create a new environmental impact.
    Returns:
        EnvironmentalImpact: The newly created EnvironmentalImpact instance.
    """
    try:
        new_impact = EnvironmentalImpact(**data)
        db.session.add(new_impact)
        db.session.commit()
        return new_impact
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating environmental impact: {e}")
        raise

def update_environmental_impact(impact_id, data):
    """
    Updates an existing environmental impact.
    Args:
        impact_id (int): The ID of the environmental impact to update.
        data (dict): A dictionary with the fields to update.
    Returns:
        EnvironmentalImpact: The updated EnvironmentalImpact instance, or None if not found.
    """
    try:
        impact = EnvironmentalImpact.query.get(impact_id)
        if impact:
            for key, value in data.items():
                setattr(impact, key, value)
            db.session.commit()
            return impact
        else:
            return None
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating environmental impact with ID {impact_id}: {e}")
        raise

def delete_environmental_impact(impact_id):
    """
    Deletes an environmental impact from the database.
    Args:
        impact_id (int): The ID of the environmental impact to delete.
    """
    try:
        impact = EnvironmentalImpact.query.get(impact_id)
        if impact:
            db.session.delete(impact)
            db.session.commit()
        else:
            logger.warning(f"No environmental impact found with ID {impact_id} to delete.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting environmental impact with ID {impact_id}: {e}")
        raise