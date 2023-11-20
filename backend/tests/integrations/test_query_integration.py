import pytest
from app import create_app
from app.models import Material, GeneralCategory

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

def test_run_query_material_name(test_client):

    material = Material.query.filter_by(materialname="Gallium Arsenide").first()
    assert material is not None  

  
    response = test_client.post('/api/query/', json={
        'material': {'materialname': material.materialname},
    })

    assert response.status_code == 200
    query_results = response.get_json()
    assert query_results is not None
    assert any(result['materialname'] == material.materialname for result in query_results)

def test_run_query_with_company_filter(test_client):

    company_name = "Company A"
    filter_data = {'company': {'companyname': company_name}}

    response = test_client.post('/api/query/', json=filter_data)

    assert response.status_code == 200
    results = response.get_json()
    assert all(company['companyname'] == company_name for company in results)

def test_run_query_with_environmental_filter(test_client):
    recyclable = True
    filter_data = {'environmental': {'recyclability': recyclable}}

    response = test_client.post('/api/query/', json=filter_data)

    assert response.status_code == 200
    results = response.get_json()

    assert all(env['recyclable'] == recyclable for env in results if 'recyclable' in env)

def test_run_query_with_sold_by_filter(test_client):
    company_id = 1  
    filter_data = {'sold_by': {'companyid': company_id}}

    response = test_client.post('/api/query/', json=filter_data)

    assert response.status_code == 200
    results = response.get_json()

    assert all('sold_by' in result and any(sold['companyid'] == company_id for sold in result['sold_by']) for result in results)


def test_run_query_with_combined_filters(test_client):

    material_name = "Gallium Arsenide"
    company_name = "Company A"
    recyclable = True
    filter_data = {
        'material': {'materialname': material_name},
        'company': {'companyname': company_name},
        'environmental': {'recyclability': recyclable}
    }

    response = test_client.post('/api/query/', json=filter_data)

    assert response.status_code == 200
    results = response.get_json()

    assert all(
        result['materialname'] == material_name and
        result['companyname'] == company_name and
        result['recyclability'] is recyclable
        for result in results
    )

def test_run_query_no_results(test_client):

    filter_data = {'material': {'materialname': "Nonexistent Material"}}


    response = test_client.post('/api/query/', json=filter_data)


    assert response.status_code == 200
    results = response.get_json()
    assert len(results) == 0

if __name__ == "__main__":
    pytest.main(['-vv', 'test_query_integration.py'])