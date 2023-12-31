import pytest
from unittest.mock import patch
from app.app import create_app
from app.services.sold_by_service import (
    get_all_sold_by_relations,
    get_sold_by_relation,
    create_sold_by_relation,
    update_sold_by_relation,
    delete_sold_by_relation
)
from app.models.sold_by_model import SoldBy

app = create_app()
app.config['TESTING'] = True

@pytest.fixture
def sample_sold_by_relations():
    sold_by_a = SoldBy(MaterialID=1, CompanyID=1, BasePrice=100, Currency='USD')
    sold_by_b = SoldBy(MaterialID=2, CompanyID=2, BasePrice=200, Currency='EUR')
    return [sold_by_a, sold_by_b]

@pytest.fixture(scope="module")
def app_context():
    with app.app_context():
        yield

def test_get_all_sold_by_relations(sample_sold_by_relations, app_context):
    with patch('app.models.sold_by_model.SoldBy.query') as mock_query:
        mock_query.return_value.all.return_value = sample_sold_by_relations
        relations = get_all_sold_by_relations()
        assert len(relations) == 0

def test_get_sold_by_relation_found(sample_sold_by_relations, app_context):
    with patch('app.models.sold_by_model.SoldBy.query') as mock_query:
        mock_query.return_value.get.return_value = sample_sold_by_relations[0]
        relation = get_sold_by_relation(1, 1)
        assert relation is not None

def test_get_sold_by_relation_not_found(sample_sold_by_relations, app_context):
    with patch('app.models.sold_by_model.SoldBy.query') as mock_query:
        mock_query.return_value.get.return_value = None
        relation = get_sold_by_relation(999, 999)
        assert relation is not None