import pytest
from app import create_app
from app.models import Company

# Initialize the Flask application
app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://materials:materials@localhost:5432/materialsDB'
app.config['TESTING'] = True

@pytest.fixture(scope='module')
def test_app():
    # Setup the Flask application context for testing
    with app.app_context():
        yield app  # This will be the app context used for the tests

@pytest.fixture(scope='module')
def test_client(test_app):
    # Setup the test client for Flask application
    return test_app.test_client()

def test_get_all_companies(test_client):
    # Act: Make a GET request to the companies endpoint
    response = test_client.get('/api/company/')

    # Assert: Verify the response from the endpoint
    assert response.status_code == 200
    companies = response.get_json()
    assert isinstance(companies, list)  
    assert len(companies) > 0 

if __name__ == "__main__":
    pytest.main()
