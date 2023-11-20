from flask import Blueprint, jsonify, request, abort
from app import db
from app.services.industrial_service import (
    get_all_applications,
    get_application_by_id
)
import logging

logger = logging.getLogger('industrial_routes')

industrial_bp = Blueprint('industrial', __name__, url_prefix='/api/industrial')

@industrial_bp.route('/', methods=['GET'])
def get_applications():
    try:
        applications = get_all_applications()
        return applications
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