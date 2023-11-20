import json
from unittest.mock import patch
from flask import Flask
from app import create_app  
from app.models.industrial_model import IndustrialApplication  

app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

sample_applications = [
    IndustrialApplication(MaterialID=1, ApplicationName='Insulation', Industry='Construction'),
    IndustrialApplication(MaterialID=2, ApplicationName='Conductor', Industry='Electronics')
]
sample_applications[0].ApplicationID = 1
sample_applications[1].ApplicationID = 2

mock_all_query = sample_applications
mock_single_query = sample_applications[0]

def test_get_industrial_applications():
    with app.app_context():
        with patch('app.models.industrial_model.IndustrialApplication.query') as mock_query:
            mock_query.all.return_value = sample_applications
            with app.test_client() as client:
                response = client.get('/api/industrial/')
                assert response.status_code == 200
                data = json.loads(response.data.decode())
                assert data == [
                    {"application_id": 1, "material_id": 1, "application_name": "Insulation", "industry": "Construction"},
                    {"application_id": 2, "material_id": 2, "application_name": "Conductor", "industry": "Electronics"}
                ]

def test_get_industrial_application():
    with app.app_context():
        with patch('app.models.industrial_model.IndustrialApplication.query') as mock_query:
            mock_query.get.return_value = mock_single_query
            with app.test_client() as client:
                response = client.get('/api/industrial/1')
                assert response.status_code == 200
                data = json.loads(response.data.decode())
                assert data == {"application_id": 1, "material_id": 1, "application_name": "Insulation", "industry": "Construction"}

