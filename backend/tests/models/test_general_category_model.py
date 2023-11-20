import json
from unittest.mock import patch
from app import create_app 
from app.models.general_categories_model import GeneralCategory 

app = create_app()
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

sample_categories = [
    GeneralCategory(CategoryName='Electronics'),
    GeneralCategory(CategoryName='Construction')
]
sample_categories[0].GeneralCategoryID = 1
sample_categories[1].GeneralCategoryID = 2

mock_all_query = sample_categories
mock_single_query = sample_categories[0]

def test_get_general_categories():
    with app.app_context():
        with patch('app.models.general_categories_model.GeneralCategory.query') as mock_query:
            mock_query.all.return_value = mock_all_query
            with app.test_client() as client:
                response = client.get('/api/general_categories/')
                assert response.status_code == 200
                data = json.loads(response.data.decode())
                assert data == [
                    {"general_category_id": 1, "category_name": "Electronics"},
                    {"general_category_id": 2, "category_name": "Construction"}
                ]

def test_get_general_category():
    with app.app_context():
        with patch('app.models.general_categories_model.GeneralCategory.query') as mock_query:
            mock_query.get.return_value = mock_single_query
            with app.test_client() as client:
                response = client.get('/api/general_categories/1')
                assert response.status_code == 200
                data = json.loads(response.data.decode())
                assert data == {"general_category_id": 1, "category_name": "Electronics"}
