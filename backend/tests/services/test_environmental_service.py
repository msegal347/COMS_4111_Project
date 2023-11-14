import pytest
from unittest.mock import patch
from app.services.environmental_service import (
    get_all_environmental_impacts,
    get_environmental_impact_by_id,
    create_environmental_impact,
    update_environmental_impact,
    delete_environmental_impact
)
from app.models.environmental_model import EnvironmentalImpact
from app.app import create_app

@pytest.fixture
def app():
    """Fixture for creating a Flask app."""
    _app = create_app()
    _app.config['TESTING'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return _app

@pytest.fixture
def sample_impacts(app):
    """Fixture for creating sample environmental impacts."""
    with app.app_context():
        _sample_impacts = [
            EnvironmentalImpact(MaterialID=1, ToxicityLevel=5.0, Recyclability=True, CarbonFootprint=100.0),
            EnvironmentalImpact(MaterialID=2, ToxicityLevel=3.0, Recyclability=False, CarbonFootprint=200.0)
        ]
        _sample_impacts[0].ImpactID = 1
        _sample_impacts[1].ImpactID = 2
        return _sample_impacts

def test_get_all_environmental_impacts(app, sample_impacts):
    with app.app_context():
        with patch('app.models.environmental_model.EnvironmentalImpact.query') as mock_query:
            mock_query.all.return_value = sample_impacts
            impacts = get_all_environmental_impacts()
            assert len(impacts) == 2
            assert impacts[0].ToxicityLevel == 5.0
            assert impacts[1].ToxicityLevel == 3.0

def test_get_environmental_impact_by_id_found(app, sample_impacts):
    with app.app_context():
        with patch('app.models.environmental_model.EnvironmentalImpact.query') as mock_query:
            mock_query.get.return_value = sample_impacts[0]
            impact = get_environmental_impact_by_id(1)
            assert impact is not None
            assert impact.ToxicityLevel == 5.0

def test_get_environmental_impact_by_id_not_found(app, sample_impacts):
    with app.app_context():
        with patch('app.models.environmental_model.EnvironmentalImpact.query') as mock_query:
            mock_query.get.return_value = None
            impact = get_environmental_impact_by_id(3)
            assert impact is None

def test_create_environmental_impact(app, sample_impacts):
    new_impact_data = {
        'MaterialID': 3,
        'ToxicityLevel': 7.0,
        'Recyclability': True,
        'CarbonFootprint': 150.0
    }
    with app.app_context():
        with patch('app.extensions.db.session.add'), patch('app.extensions.db.session.commit'):
            new_impact = create_environmental_impact(new_impact_data)
            assert new_impact.MaterialID == 3
            assert new_impact.ToxicityLevel == 7.0

def test_update_environmental_impact_found(app, sample_impacts):
    update_data = {'ToxicityLevel': 8.0}
    with app.app_context():
        with patch('app.models.environmental_model.EnvironmentalImpact.query') as mock_query:
            mock_query.get.return_value = sample_impacts[0]
            updated_impact = update_environmental_impact(1, update_data)
            assert updated_impact is not None
            assert updated_impact.ToxicityLevel == 8.0

def test_delete_environmental_impact_found(app, sample_impacts):
    with app.app_context():
        with patch('app.models.environmental_model.EnvironmentalImpact.query') as mock_query, \
             patch('app.extensions.db.session.delete'), \
             patch('app.extensions.db.session.commit'):
            mock_query.get.return_value = sample_impacts[0]
            delete_environmental_impact(1)
