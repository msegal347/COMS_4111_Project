import json
from unittest.mock import patch
from flask import Flask
from app.models.environmental_model import EnvironmentalImpact

# Adjust the imports according to your directory structure
from app import create_app

# Initialize the Flask application for testing
app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing

# Sample environmental impact data
sample_impacts = [
    EnvironmentalImpact(materialid=1, toxicitylevel=5.0, recyclability=True, carbonfootprint=100.0),
    EnvironmentalImpact(materialid=2, toxicitylevel=3.0, recyclability=False, carbonfootprint=200.0)
]
sample_impacts[0].impactid = 1
sample_impacts[1].impactid = 2

# Test for GET all environmental impacts
def test_get_environmental_impacts():
    with app.app_context():
        with patch('app.models.environmental_model.EnvironmentalImpact.query') as mock_query:
            mock_query.all.return_value = sample_impacts
            with app.test_client() as client:
                response = client.get('/api/environmental/')
                if response.status_code != 200:
                    print(response.data)  # This will print out the error details
                assert response.status_code == 200

