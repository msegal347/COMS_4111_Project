import pytest
from app import create_app, db
from app.models import Material, SoldBy, Company

app = create_app()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://materials:materials@localhost:5432/materialsDB'
app.config['TESTING'] = True

@pytest.fixture(scope='module')
def test_app():
    with app.app_context():
        db.create_all() 
        yield app  
        db.session.remove()

@pytest.fixture(scope='module')
def test_client(test_app):
    return test_app.test_client()

def test_get_sold_by_relations(test_client, test_app):
    response = test_client.get('/api/sold_by/')
    assert response.status_code == 200
    sold_by_relations = response.get_json()
    assert sold_by_relations is not None
    assert type(sold_by_relations) is list
    assert len(sold_by_relations) > 0

if __name__ == "__main__":
    pytest.main()