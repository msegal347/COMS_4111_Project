from app.extensions import db
from app.models.industrial_model import IndustrialApplication
import logging

# Set up logger
logger = logging.getLogger('industrial_service')

def get_all_applications():
    """
    Retrieves all industrial applications from the database.
    Returns:
        List[IndustrialApplication]: A list of IndustrialApplication instances.
    """
    try:
        return IndustrialApplication.query.all()
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
    try:
        return IndustrialApplication.query.get(application_id)
    except Exception as e:
        logger.error(f"Error retrieving industrial application with ID {application_id}: {e}")
        raise

def create_application(data):
    """
    Creates a new industrial application record in the database.
    Args:
        data (dict): A dictionary with the required fields to create a new industrial application.
    Returns:
        IndustrialApplication: The newly created IndustrialApplication instance.
    """
    try:
        new_application = IndustrialApplication(**data)
        db.session.add(new_application)
        db.session.commit()
        return new_application
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating industrial application: {e}")
        raise

def update_application(application_id, data):
    """
    Updates an existing industrial application.
    Args:
        application_id (int): The ID of the industrial application to update.
        data (dict): A dictionary with the fields to update.
    Returns:
        IndustrialApplication: The updated IndustrialApplication instance, or None if not found.
    """
    try:
        application = IndustrialApplication.query.get(application_id)
        if application:
            for key, value in data.items():
                setattr(application, key, value)
            db.session.commit()
            return application
        else:
            return None
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating industrial application with ID {application_id}: {e}")
        raise

def delete_application(application_id):
    """
    Deletes an industrial application from the database.
    Args:
        application_id (int): The ID of the industrial application to delete.
    """
    try:
        application = IndustrialApplication.query.get(application_id)
        if application:
            db.session.delete(application)
            db.session.commit()
        else:
            logger.warning(f"No industrial application found with ID {application_id} to delete.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting industrial application with ID {application_id}: {e}")
        raise
