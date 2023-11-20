import json
from unittest.mock import patch
from app import create_app
from app.models.company_model import Company

app = create_app()
app.config['TESTING'] = True

sample_companies = [
    Company(companyname="Company A", location="Location A"),
    Company(companyname="Company B", location="Location B")
]

sample_companies[0].companyid = 1
sample_companies[1].companyid = 2

mock_all_query = sample_companies
mock_single_query = sample_companies[0]

def test_get_companies():
    with patch('app.extensions.db.session.query') as mock_query:
        mock_query.return_value.all.return_value = mock_all_query
        with app.test_client() as client:
            response = client.get('/api/company/')
            assert response.status_code == 200
            assert response.is_json
            data = response.get_json()
            assert data == [
                {"id": 1, "name": "Company A", "location": "Location A", "subsidiary": None},
                {"id": 2, "name": "Company B", "location": "Location B", "subsidiary": None}
            ]

def test_get_company():
    with patch('app.extensions.db.session.query') as mock_query:
        mock_query.return_value.filter_by.return_value.first.return_value = mock_single_query
        with app.test_client() as client:
            response = client.get('/api/company/1')
            assert response.status_code == 200
            assert response.is_json
            data = response.get_json()
            assert data == {"id": 1, "name": "Company A", "location": "Location A", "subsidiary": None}
