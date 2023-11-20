import pytest
from app import create_app
from app.models import Company

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

def test_get_all_companies(test_client):
    response = test_client.get('/api/company/')

    assert response.status_code == 200
    companies = response.get_json()
    assert isinstance(companies, list)  
    assert len(companies) > 0 

if __name__ == "__main__":
    pytest.main()
