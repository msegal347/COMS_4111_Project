import json
from unittest.mock import patch
from app import create_app  # Adjust the import according to your directory structure
from app.models.sold_by_model import SoldBy  # Adjust the import according to your directory structure

# Initialize the Flask application for testing
app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# Sample sold by relationship data
sample_sold_by = [
    SoldBy(MaterialID=1, CompanyID=100, BasePrice=10.0, Currency='USD'),
    SoldBy(MaterialID=2, CompanyID=200, BasePrice=20.0, Currency='EUR')
]
sample_sold_by[0].MaterialID = 1
sample_sold_by[0].CompanyID = 100
sample_sold_by[1].MaterialID = 2
sample_sold_by[1].CompanyID = 200

# Mock query responses
mock_all_query = sample_sold_by
mock_single_query = sample_sold_by[0]

# Test for GET all sold by relationships
def test_get_sold_by():
    with app.app_context():
        with patch('app.models.sold_by_model.SoldBy.query') as mock_query:
            mock_query.all.return_value = mock_all_query
            with app.test_client() as client:
                response = client.get('/api/sold_by/')
                assert response.status_code == 200
                data = json.loads(response.data.decode())
                assert data == [
                    {"material_id": 1, "company_id": 100, "base_price": 10.0, "currency": "USD"},
                    {"material_id": 2, "company_id": 200, "base_price": 20.0, "currency": "EUR"}
                ]

# Test for GET a single sold by relationship by MaterialID and CompanyID
def test_get_sold_by_single():
    with app.app_context():
        with patch('app.models.sold_by_model.SoldBy.query') as mock_query:
            mock_query.get.return_value = mock_single_query
            with app.test_client() as client:
                response = client.get('/api/sold_by/1/100')
                assert response.status_code == 200
                data = json.loads(response.data.decode())
                assert data == {"material_id": 1, "company_id": 100, "base_price": 10.0, "currency": "USD"}
