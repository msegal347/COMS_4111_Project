import pytest
from unittest.mock import patch
from app.services.material_service import get_all_materials, get_material_by_id
from app.models.material_model import Material
from datetime import datetime

@pytest.fixture
def sample_materials():

    material_a = Material(materialname="Material A", generalcategoryid=1)
    material_b = Material(materialname="Material B", generalcategoryid=2)
    return [material_a, material_b]

def test_get_all_materials(sample_materials):
    with patch('app.extensions.db.session.query') as mock_query:
        mock_query.return_value.all.return_value = sample_materials
        materials = get_all_materials()
        assert len(materials) == 2
        assert materials[0]['name'] == "Material A"
        assert materials[0]['general_category_id'] == 1


def test_get_material_by_id_not_found():
    with patch('app.extensions.db.session.query') as mock_query:
        mock_query.return_value.filter_by.return_value.first.return_value = None
        material = get_material_by_id(999)
        assert material is None
