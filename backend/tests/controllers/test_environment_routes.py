import pytest
from unittest.mock import patch
from flask import Flask, jsonify
from app.app import create_app
from app.models.environmental_model import EnvironmentalImpact

# Initialize the Flask application for testing
app = create_app()
app.config['TESTING'] = True
app.config['SERVER_NAME'] = 'localhost.local'

@pytest.fixture(scope="module")
def client():
    with app.app_context():
        with app.test_client() as c:
            yield c

# Fixture for creating sample environmental impacts
@pytest.fixture
def sample_environmental_impacts():
    impact_a = EnvironmentalImpact(MaterialID=1, ToxicityLevel=5, Recyclability=True, CarbonFootprint=100)
    impact_b = EnvironmentalImpact(MaterialID=2, ToxicityLevel=3, Recyclability=False, CarbonFootprint=200)
    impact_a.ImpactID = 1
    impact_b.ImpactID = 2
    return [impact_a, impact_b]

# Test for GET all environmental impacts route
def test_get_environmental_impacts_route(client, sample_environmental_impacts):
    with patch('app.models.environmental_model.EnvironmentalImpact.query') as mock_query:
        mock_query.all.return_value = sample_environmental_impacts
        response = client.get('/api/environmental/')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['toxicity_level'] == 5
        assert data[1]['toxicity_level'] == 3

# Test for GET a single environmental impact by ID route when the impact is found
def test_get_environmental_impact_route_found(client, sample_environmental_impacts):
    with patch('app.models.environmental_model.EnvironmentalImpact.query') as mock_query:
        mock_query.get_or_404.return_value = sample_environmental_impacts[0]
        response = client.get('/api/environmental/1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['toxicity_level'] == 5

# Test for GET a single environmental impact by ID route when the impact is not found
def test_get_environmental_impact_route_not_found(client):
    with patch('app.models.environmental_model.EnvironmentalImpact.query') as mock_query:
        mock_query.return_value.filter_by.return_value.first.return_value = None 
        response = client.get('/api/environmental/999')
        assert response.status_code == 500
