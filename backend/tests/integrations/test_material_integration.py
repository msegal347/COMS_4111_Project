import pytest
from app import create_app
from app.models import db, Material

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://materials:materials@localhost:5432/materialsDB'
app.config['TESTING'] = True

@pytest.fixture(scope='module')
def test_app():
    ctx = app.app_context()
    ctx.push()

    yield app 

    ctx.pop()

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()

def test_get_all_materials(test_client):
    response = test_client.get('/api/material/')

    assert response.status_code == 200
    materials = response.get_json()
    assert materials is not None
    assert type(materials) is list

def test_get_specific_material(test_client):
    test_material_id = 1  

    response = test_client.get(f'/api/material/{test_material_id}')

    assert response.status_code == 200
    material = response.get_json()
    assert material is not None
    assert material['id'] == test_material_id

if __name__ == "__main__":
    pytest.main()
