import pytest
from app import create_app, db

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://materials:materials@localhost:5432/materialsDB'
app.config['TESTING'] = True

@pytest.fixture(scope='module')
def test_app():
    with app.app_context():
        # Normally, db.create_all() would be called here, but we are not modifying the database
        yield app  # This will be the app context used in tests

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()

def test_get_all_general_categories(test_client):
    # Act: Make a request to the get_categories endpoint
    response = test_client.get('/api/general_categories/')

    # Assert: Verify the response from the endpoint
    assert response.status_code == 200
    categories = response.get_json()
    # Assuming the test database is pre-populated, check that at least one category is returned
    assert len(categories) > 0
    # Optionally, check for specific category names if known
    category_names = {category['categoryname'] for category in categories}
    assert 'Metals' in category_names
    assert 'Polymers' in category_names

if __name__ == "__main__":
    pytest.main()
