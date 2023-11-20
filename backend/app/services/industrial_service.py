from app.extensions import db
from app.models.industrial_model import IndustrialApplication
from app.models.has_practical_uses_model import HasPracticalUses 
import logging

logger = logging.getLogger('industrial_service')

def get_all_applications():
    """
    Retrieves all industrial applications from the database.
    Returns:
        List[dict]: A list of dictionaries containing industrial application data.
    """
    try:
        industrial_query = db.session.query(
            IndustrialApplication.applicationid,
            IndustrialApplication.applicationname,
            IndustrialApplication.industry
        ).all()

        return [
            {
                "id": application_id,
                "application_name": application_name,
                "industry": industry
            }
            for application_id, application_name, industry in industrial_query
        ]
    except Exception as e:
        logger.error(f"Error retrieving all industrial applications: {e}")
        raise

def get_application_by_id(application_id):
    """
    Retrieves an industrial application by its ID.
    Args:
        application_id (int): The ID of the industrial application to retrieve.
    Returns:
        dict: A dictionary containing the industrial application data if found, otherwise None.
    """
    try:
        industrial_app = IndustrialApplication.query.get(application_id)
        if industrial_app:
            return industrial_app.to_dict()
        return None
    except Exception as e:
        logger.error(f"Error retrieving industrial application with ID {application_id}: {e}")
        raise
