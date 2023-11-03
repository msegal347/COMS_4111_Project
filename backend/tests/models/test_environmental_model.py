import json
from unittest.mock import patch
from flask import Flask
from app.models.environmental_model import EnvironmentalImpact

# Adjust the imports according to your directory structure
from app.app import create_app

# Initialize the Flask application for testing
app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing

# Sample environmental impact data
sample_impacts = [
    EnvironmentalImpact(MaterialID=1, ToxicityLevel=5.0, Recyclability=True, CarbonFootprint=100.0),
    EnvironmentalImpact(MaterialID=2, ToxicityLevel=3.0, Recyclability=False, CarbonFootprint=200.0)
]
sample_impacts[0].ImpactID = 1
sample_impacts[1].ImpactID = 2

# Test for GET all environmental impacts
def test_get_environmental_impacts():
    # Push an application context for the current app
    with app.app_context():
        # Use the correct reference to the query object. If it's not directly EnvironmentalImpact.query,
        # adjust the path below to match where it's imported from.
        with patch('app.models.environmental_model.EnvironmentalImpact.query') as mock_query:
            mock_query.all.return_value = sample_impacts
            with app.test_client() as client:
                response = client.get('/api/environmental/')
                assert response.status_code == 200
                data = json.loads(response.data.decode())
                assert data == [
                    {
                        "impact_id": 1,
                        "material_id": 1,
                        "toxicity_level": 5.0,
                        "recyclability": True,
                        "carbon_footprint": 100.0
                    },
                    {
                        "impact_id": 2,
                        "material_id": 2,
                        "toxicity_level": 3.0,
                        "recyclability": False,
                        "carbon_footprint": 200.0
                    }
                ]
