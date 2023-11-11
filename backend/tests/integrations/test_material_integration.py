import pytest
from app import create_app
from app.models import db, Material

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://materials:materials@localhost:5432/materialsDB'
app.config['TESTING'] = True

@pytest.fixture(scope='module')
def test_app():
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield app 

    # After the tests run, you can tear down the test data or drop tables as needed.
    ctx.pop()

@pytest.fixture(scope='module')
def test_client(test_app):
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    return test_app.test_client()

def test_get_all_materials(test_client):
    # Make a request to the get_materials endpoint.
    response = test_client.get('/api/material/')

    # Check the response for a list of materials.
    assert response.status_code == 200
    materials = response.get_json()
    assert materials is not None
    assert type(materials) is list  # Ensure that a list is returned

def test_get_specific_material(test_client):
    # You need to know the ID of a material that exists in the test database.
    test_material_id = 1  # Example ID, replace with a valid ID from your test database.

    # Make a request to the get_material endpoint with a known ID.
    response = test_client.get(f'/api/material/{test_material_id}')

    # Check the response for the specific material details.
    assert response.status_code == 200
    material = response.get_json()
    assert material is not None
    assert material['id'] == test_material_id  # Ensure the correct material is returned

# Add this if you want to run the tests with Python directly instead of using pytest from the command line.
if __name__ == "__main__":
    pytest.main()
