import pytest
from app import create_app
from app.models import db, Material, IndustrialApplication

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://materials:materials@localhost:5432/materialsDB'
app.config['TESTING'] = True

@pytest.fixture(scope='module')
def test_app():
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    yield app 
    ctx.pop()

@pytest.fixture(scope='module')
def test_client(test_app):
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    return test_app.test_client()

def test_get_all_applications(test_client):
    response = test_client.get('/api/industrial/')
    assert response.status_code == 200
    applications = response.get_json()
    assert applications is not None
    assert type(applications) is list

def test_get_specific_application(test_client):
    test_application_id = 1  # Replace with a valid ID from your test database.
    response = test_client.get(f'/api/industrial/{test_application_id}')
    assert response.status_code == 200
    application = response.get_json()
    assert application is not None
    # Use the correct key as defined in your to_dict method of IndustrialApplication model
    assert application['applicationid'] == test_application_id

if __name__ == "__main__":
    pytest.main()
