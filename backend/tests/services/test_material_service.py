import pytest
from unittest.mock import patch
from app.services.material_service import get_all_materials, get_material_by_id
from app.models.material_model import Material

# Fixture for creating sample materials
@pytest.fixture
def sample_materials():
    material_a = Material(MaterialName="Material A", GeneralCategoryID=1, ElementalComposition="H2O", MolecularWeight=18.015)
    material_b = Material(MaterialName="Material B", GeneralCategoryID=2, ElementalComposition="CO2", MolecularWeight=44.01)
    material_a.MaterialID = 1
    material_b.MaterialID = 2
    return [material_a, material_b]


# Test for get_all_materials service function
def test_get_all_materials(sample_materials):
    with patch('app.extensions.db.session.query') as mock_query:
        mock_query.return_value.all.return_value = sample_materials
        materials = get_all_materials()
        assert len(materials) == 2
        assert materials[0]['name'] == "Material A"
        assert materials[1]['name'] == "Material B"

# Test for get_material_by_id service function when material is found
def test_get_material_by_id_found(sample_materials):
    with patch('app.extensions.db.session.query') as mock_query:
        mock_query.return_value.filter_by.return_value.first.return_value = sample_materials[0]
        material = get_material_by_id(1)
        assert material is not None
        assert material['name'] == "Material A"

# Test for get_material_by_id service function when material is not found
def test_get_material_by_id_not_found(sample_materials):
    with patch('app.extensions.db.session.query') as mock_query:
        mock_query.return_value.filter_by.return_value.first.return_value = None
        material = get_material_by_id(999)
        assert material is None
