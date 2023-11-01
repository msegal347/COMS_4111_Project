import json
from unittest.mock import patch
from app.app import create_app  # Adjust the import according to your directory structure
from app.models.material_model import Material  # Adjust the import according to your directory structure

# Initialize the Flask application for testing
app = create_app()
app.config['TESTING'] = True

# Sample material data
sample_materials = [
    Material(MaterialName="Material A", GeneralCategoryID=1),
    Material(MaterialName="Material B", GeneralCategoryID=2)
]
sample_materials[0].MaterialID = 1
sample_materials[1].MaterialID = 2

# Mock query responses
mock_all_query = sample_materials
mock_single_query = sample_materials[0]

# Test for GET all materials
def test_get_materials():
    with patch('app.extensions.db.session.query') as mock_query:
        mock_query.return_value.all.return_value = mock_all_query
        with app.test_client() as client:
            response = client.get('/api/material/')
            data = json.loads(response.data.decode())
            assert response.status_code == 200
            assert data == [
                {
                    "id": 1, 
                    "name": "Material A", 
                    "general_category_id": 1,
                    "created_at": None,
                    "updated_at": None,
                    "elemental_composition": None,
                    "molecular_weight": None,
                    "tensile_strength": None,
                    "ductility": None,
                    "hardness": None,
                    "thermal_conductivity": None,
                    "heat_capacity": None,
                    "melting_point": None,
                    "refractive_index": None,
                    "absorbance": None,
                    "conductivity": None,
                    "resistivity": None
                },
                {
                    "id": 2, 
                    "name": "Material B", 
                    "general_category_id": 2,
                    "created_at": None,
                    "updated_at": None,
                    "elemental_composition": None,
                    "molecular_weight": None,
                    "tensile_strength": None,
                    "ductility": None,
                    "hardness": None,
                    "thermal_conductivity": None,
                    "heat_capacity": None,
                    "melting_point": None,
                    "refractive_index": None,
                    "absorbance": None,
                    "conductivity": None,
                    "resistivity": None
                }
            ]

# Test for GET a single material by ID
def test_get_material():
    with patch('app.extensions.db.session.query') as mock_query:
        mock_query.return_value.filter_by.return_value.first.return_value = mock_single_query
        with app.test_client() as client:
            response = client.get('/api/material/1')
            data = json.loads(response.data.decode())
            assert response.status_code == 200
            assert data == {
                "id": 1, 
                "name": "Material A", 
                "general_category_id": 1,
                "created_at": None,
                "updated_at": None,
                "elemental_composition": None,
                "molecular_weight": None,
                "tensile_strength": None,
                "ductility": None,
                "hardness": None,
                "thermal_conductivity": None,
                "heat_capacity": None,
                "melting_point": None,
                "refractive_index": None,
                "absorbance": None,
                "conductivity": None,
                "resistivity": None
            }
