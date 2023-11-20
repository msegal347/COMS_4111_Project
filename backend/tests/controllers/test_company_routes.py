import pytest
from unittest.mock import patch
from flask import jsonify
from app.app import create_app
from app.models.company_model import Company

app = create_app()
app.config['TESTING'] = True
app.config['SERVER_NAME'] = 'localhost.local'

@pytest.fixture
def sample_companies():
    company_a = Company(CompanyName="Company A", Location="Location A")
    company_b = Company(CompanyName="Company B", Location="Location B")
    company_a.CompanyID = 1
    company_b.CompanyID = 2
    return [company_a, company_b]

def test_get_companies_route(sample_companies):
    with patch('app.models.company_model.db.session.query') as mock_query:
        mock_query.return_value.all.return_value = sample_companies
        with app.test_client() as client:
            response = client.get('/api/company/')
            assert response.status_code == 200
            data = response.get_json()
            assert len(data) == 2
            assert data[0]['name'] == "Company A"
            assert data[1]['name'] == "Company B"

def test_get_company_route_found(sample_companies):
    with patch('app.models.company_model.db.session.query') as mock_query:
        mock_query.return_value.filter_by.return_value.first.return_value = sample_companies[0]
        with app.test_client() as client:
            response = client.get('/api/company/1')
            assert response.status_code == 200
            data = response.get_json()
            assert data['name'] == "Company A"

def test_get_company_route_not_found():
    with patch('app.models.company_model.db.session.query') as mock_query:
        mock_query.return_value.filter_by.return_value.first.return_value = None
        with app.test_client() as client:
            response = client.get('/api/company/999')
            assert response.status_code == 500
