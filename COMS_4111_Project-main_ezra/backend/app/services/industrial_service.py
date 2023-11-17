from app.extensions import db
from app.models.industrial_model import IndustrialApplication
from app.models.material_model import Material
import logging

# Set up logger
logger = logging.getLogger('industrial_service')
print('nothing?')
def get_all_applications():
    """
    Retrieves all industrial applications from the database.
    Returns:
        List[IndustrialApplication]: A list of IndustrialApplication instances.
    """
    try:
        # Use IndustrialApplication class for querying
        industrial_query = db.session.query(IndustrialApplication,Material.materialname).join(
            Material,
            IndustrialApplication.materialid == Material.materialid
        ).all()
        return [
        {
            "id": industry.IndustrialApplication.applicationid,
            "material_name": industry.materialname,
            "application_name": industry.IndustrialApplication.applicationname,
            "industry": industry.IndustrialApplication.industry
        }
        for industry in industrial_query
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
        IndustrialApplication: An instance of IndustrialApplication if found, otherwise None.
    """
    print('looks like we got here though')
    try:
        # Use IndustrialApplication class for querying
        return IndustrialApplication.query.get(application_id)
    except Exception as e:
        logger.error(f"Error retrieving industrial application with ID {application_id}: {e}")
        raise
