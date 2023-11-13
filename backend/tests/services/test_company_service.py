import pytest
from unittest.mock import patch
from app.services.company_service import get_all_companies, get_company_by_id
from app.models.company_model import Company
from app.app import create_app

@pytest.fixture
def app():
    """Fixture for creating a Flask app."""
    _app = create_app()
    _app.config['TESTING'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return _app

@pytest.fixture
def sample_companies(app):
    """Fixture for creating sample companies."""
    with app.app_context():
        _sample_companies = [
            Company(CompanyName="Company A", Location="Location A"),
            Company(CompanyName="Company B", Location="Location B")
        ]
        _sample_companies[0].CompanyID = 1
        _sample_companies[1].CompanyID = 2
        return _sample_companies

def test_get_all_companies(app, sample_companies):
    with app.app_context():
        with patch('app.extensions.db.session.query') as mock_query:
            mock_query.return_value.all.return_value = sample_companies
            companies = get_all_companies()
            assert len(companies) == 2
            assert companies[0]['name'] == "Company A"
            assert companies[1]['name'] == "Company B"

def test_get_company_by_id_found(app, sample_companies):
    with app.app_context():
        with patch('app.extensions.db.session.query') as mock_query:
            mock_query.return_value.filter_by.return_value.first.return_value = sample_companies[0]
            company = get_company_by_id(1)
            assert company is not None
            assert company['name'] == "Company A"

def test_get_company_by_id_not_found(app, sample_companies):
    with app.app_context():
        with patch('app.extensions.db.session.query') as mock_query:
            mock_query.return_value.filter_by.return_value.first.return_value = None
            company = get_company_by_id(3)
            assert company is None
