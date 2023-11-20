import pytest
from app import create_app, db

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://materials:materials@localhost:5432/materialsDB'
app.config['TESTING'] = True

@pytest.fixture(scope='module')
def test_app():
    with app.app_context():
        yield app 

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()

def test_get_all_general_categories(test_client):
    response = test_client.get('/api/general_categories/')

    assert response.status_code == 200
    categories = response.get_json()
    assert len(categories) > 0
    category_names = {category['categoryname'] for category in categories}
    assert 'Metals' in category_names
    assert 'Polymers' in category_names

if __name__ == "__main__":
    pytest.main()
