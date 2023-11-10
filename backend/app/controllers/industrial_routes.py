from flask import Blueprint, jsonify, request, abort
from app import db
from app.services.industrial_service import (
    get_all_applications,
    get_application_by_id,
    create_application,
    update_application,
    delete_application
)
import logging

# Set up logger
logger = logging.getLogger('industrial_routes')

# Blueprint configuration
industrial_bp = Blueprint('industrial', __name__, url_prefix='/api/industrial')

@industrial_bp.route('/', methods=['GET'])
def get_applications():
    try:
        applications = get_all_applications()
        return jsonify([app.to_dict() for app in applications]), 200
    except Exception as e:
        logger.error(f"Error fetching industrial applications: {e}")
        abort(500, description="Internal Server Error")

@industrial_bp.route('/<int:application_id>', methods=['GET'])
def get_application(application_id):
    try:
        application = get_application_by_id(application_id)
        if application is not None:
            return jsonify(application.to_dict()), 200
        else:
            abort(404, description="Industrial application not found")
    except Exception as e:
        logger.error(f"Error fetching industrial application with id {application_id}: {e}")
        abort(500, description="Internal Server Error")

@industrial_bp.route('/', methods=['POST'])
def create_new_application():
    data = request.get_json()
    try:
        new_application = create_application(data)
        return jsonify(new_application.to_dict()), 201
    except Exception as e:
        logger.error(f"Error creating new industrial application: {e}")
        abort(500, description="Internal Server Error")

@industrial_bp.route('/<int:application_id>', methods=['PUT'])
def update_existing_application(application_id):
    data = request.get_json()
    try:
        application = update_application(application_id, data)
        if application is not None:
            return jsonify(application.to_dict()), 200
        else:
            abort(404, description="Industrial application not found")
    except Exception as e:
        logger.error(f"Error updating industrial application with id {application_id}: {e}")
        abort(500, description="Internal Server Error")

@industrial_bp.route('/<int:application_id>', methods=['DELETE'])
def delete_existing_application(application_id):
    try:
        delete_application(application_id)
        return jsonify({}), 204
    except Exception as e:
        logger.error(f"Error deleting industrial application with id {application_id}: {e}")
        abort(500, description="Internal Server Error")
