import pytest
from app import create_app, db
from app.models import Material, SoldBy, Company

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://materials:materials@localhost:5432/materialsDB'
app.config['TESTING'] = True

@pytest.fixture(scope='module')
def test_app():
    with app.app_context():
        db.create_all()  # Create all database tables
        yield app  # This will be the app context used in tests
        db.session.remove()

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()

# Test functions for SoldBy API endpoints
def test_get_sold_by_relations(test_client, test_app):
    # Make a request to the sold_by endpoint to retrieve all relationships.
    response = test_client.get('/api/sold_by/')
    assert response.status_code == 200
    sold_by_relations = response.get_json()
    assert sold_by_relations is not None
    assert type(sold_by_relations) is list
    # Assuming the test database is pre-populated, the length should be greater than zero.
    assert len(sold_by_relations) > 0

if __name__ == "__main__":
    pytest.main()