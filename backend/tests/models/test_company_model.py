import json
from unittest.mock import patch
from app.app import create_app  # Adjust the import according to your directory structure
from app.models.company_model import Company  # Adjust the import according to your directory structure

# Initialize the Flask application for testing
app = create_app()
app.config['TESTING'] = True

# Sample company data
sample_companies = [
    Company(CompanyName="Company A", Location="Location A"),
    Company(CompanyName="Company B", Location="Location B")
]
sample_companies[0].CompanyID = 1
sample_companies[1].CompanyID = 2

# Mock query responses
mock_all_query = sample_companies
mock_single_query = sample_companies[0]

# Test for GET all companies
def test_get_companies():
    with patch('app.extensions.db.session.query') as mock_query:
        mock_query.return_value.all.return_value = mock_all_query
        with app.test_client() as client:
            response = client.get('/api/company/')
            data = json.loads(response.data.decode())
            assert response.status_code == 200
            assert data == [
                {"id": 1, "name": "Company A", "location": "Location A", "subsidiary": None},
                {"id": 2, "name": "Company B", "location": "Location B", "subsidiary": None}
            ]


# Test for GET a single company by ID
def test_get_company():
    with patch('app.extensions.db.session.query') as mock_query:
        mock_query.return_value.filter_by.return_value.first.return_value = mock_single_query
        with app.test_client() as client:
            response = client.get('/api/company/1')
            data = json.loads(response.data.decode())
            assert response.status_code == 200
            assert data == {"id": 1, "name": "Company A", "location": "Location A", "subsidiary": None}

