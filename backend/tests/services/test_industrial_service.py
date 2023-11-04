import pytest
from unittest.mock import patch
from app.services.industrial_service import (
    get_all_applications,
    get_application_by_id,
    create_application,
    update_application,
    delete_application
)
from app.models.industrial_model import IndustrialApplication
from app.app import create_app

@pytest.fixture
def app():
    """Fixture for creating a Flask app."""
    _app = create_app()
    _app.config['TESTING'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return _app

@pytest.fixture
def sample_applications(app):
    """Fixture for creating sample industrial applications."""
    with app.app_context():
        _sample_applications = [
            IndustrialApplication(MaterialID=1, Industry="Industry A", ApplicationName="Application A"),
            IndustrialApplication(MaterialID=2, Industry="Industry B", ApplicationName="Application B")
        ]
        _sample_applications[0].ApplicationID = 1
        _sample_applications[1].ApplicationID = 2
        return _sample_applications


def test_get_all_applications(app, sample_applications):
    with app.app_context():
        with patch('app.models.industrial_model.IndustrialApplication.query') as mock_query:
            mock_query.all.return_value = sample_applications
            applications = get_all_applications()
            assert len(applications) == 2
            assert applications[0].ApplicationName == "Application A"
            assert applications[1].ApplicationName == "Application B"

def test_get_application_by_id_found(app, sample_applications):
    with app.app_context():
        with patch('app.models.industrial_model.IndustrialApplication.query') as mock_query:
            mock_query.get.return_value = sample_applications[0]
            application = get_application_by_id(1)
            assert application is not None
            assert application.ApplicationName == "Application A"

def test_get_application_by_id_not_found(app, sample_applications):
    with app.app_context():
        with patch('app.models.industrial_model.IndustrialApplication.query') as mock_query:
            mock_query.get.return_value = None
            application = get_application_by_id(3)
            assert application is None

def test_create_application(app, sample_applications):
    data = {"MaterialID": 3, "Industry": "Industry C", "ApplicationName": "Application C"}
    with app.app_context():
        with patch('app.extensions.db.session.add'), patch('app.extensions.db.session.commit'):
            new_application = create_application(data)
            assert new_application is not None
            assert new_application.MaterialID == data['MaterialID']
            assert new_application.Industry == data['Industry']
            assert new_application.ApplicationName == data['ApplicationName']


def test_update_application_found(app, sample_applications):
    data = {"ApplicationName": "Application Updated"}
    with app.app_context():
        with patch('app.models.industrial_model.IndustrialApplication.query') as mock_query, \
             patch('app.extensions.db.session.commit'):
            mock_query.get.return_value = sample_applications[0]
            updated_application = update_application(1, data)
            assert updated_application is not None
            assert updated_application.ApplicationName == data['ApplicationName']

def test_delete_application_found(app, sample_applications):
    with app.app_context():
        with patch('app.models.industrial_model.IndustrialApplication.query') as mock_query, \
             patch('app.extensions.db.session.delete'), \
             patch('app.extensions.db.session.commit'):
            mock_query.get.return_value = sample_applications[0]
            result = delete_application(1)
            assert result is None

def test_delete_application_not_found(app, sample_applications):
    with app.app_context():
        with patch('app.models.industrial_model.IndustrialApplication.query') as mock_query, \
             patch('app.extensions.db.session.delete'), \
             patch('app.extensions.db.session.commit'):
            mock_query.get.return_value = None
            result = delete_application(3)
            assert result is None
