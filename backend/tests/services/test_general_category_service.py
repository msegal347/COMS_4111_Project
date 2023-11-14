import pytest
from unittest.mock import patch
from app.services.general_categories_service import (
    get_all_general_categories,
    get_general_category_by_id,
    create_general_category,
    update_general_category,
    delete_general_category
)
from app.models.general_categories_model import GeneralCategory
from app.app import create_app

@pytest.fixture
def app():
    """Fixture for creating a Flask app."""
    _app = create_app()
    _app.config['TESTING'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return _app

@pytest.fixture
def sample_categories(app):
    """Fixture for creating sample general categories."""
    with app.app_context():
        _sample_categories = [
            GeneralCategory(CategoryName="Category A"),
            GeneralCategory(CategoryName="Category B")
        ]
        _sample_categories[0].CategoryID = 1
        _sample_categories[1].CategoryID = 2
        return _sample_categories

def test_get_all_general_categories(app, sample_categories):
    with app.app_context():
        with patch('app.models.general_categories_model.GeneralCategory.query') as mock_query:
            mock_query.all.return_value = sample_categories
            categories = get_all_general_categories()
            assert len(categories) == 2
            assert categories[0].CategoryName == "Category A"
            assert categories[1].CategoryName == "Category B"

def test_get_general_category_by_id_found(app, sample_categories):
    with app.app_context():
        with patch('app.models.general_categories_model.GeneralCategory.query') as mock_query:
            mock_query.get.return_value = sample_categories[0]
            category = get_general_category_by_id(1)
            assert category is not None
            assert category.CategoryName == "Category A"

def test_get_general_category_by_id_not_found(app, sample_categories):
    with app.app_context():
        with patch('app.models.general_categories_model.GeneralCategory.query') as mock_query:
            mock_query.get.return_value = None
            category = get_general_category_by_id(3)
            assert category is None

def test_create_general_category(app, sample_categories):
    category_name = "Category C"
    with app.app_context():
        with patch('app.extensions.db.session.add'), patch('app.extensions.db.session.commit'):
            new_category = create_general_category(category_name)
            assert new_category is not None
            assert new_category.CategoryName == category_name

def test_update_general_category_found(app, sample_categories):
    category_name = "Category Updated"
    with app.app_context():
        with patch('app.models.general_categories_model.GeneralCategory.query') as mock_query, \
             patch('app.extensions.db.session.commit'):
            mock_query.get.return_value = sample_categories[0]
            updated_category = update_general_category(1, category_name)
            assert updated_category is not None
            assert updated_category.CategoryName == category_name

def test_delete_general_category_found(app, sample_categories):
    with app.app_context():
        with patch('app.models.general_categories_model.GeneralCategory.query') as mock_query, \
             patch('app.extensions.db.session.delete'), \
             patch('app.extensions.db.session.commit'):
            mock_query.get.return_value = sample_categories[0]
            result = delete_general_category(1)
            assert result is True

def test_delete_general_category_not_found(app, sample_categories):
    with app.app_context():
        with patch('app.models.general_categories_model.GeneralCategory.query') as mock_query, \
             patch('app.extensions.db.session.delete'), \
             patch('app.extensions.db.session.commit'):
            mock_query.get.return_value = None
            result = delete_general_category(3)
            assert result is False
