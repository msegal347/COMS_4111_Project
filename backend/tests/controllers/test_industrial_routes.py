import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, event
from sqlalchemy.engine import Engine

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost.local'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

app = create_app()

from app.models.general_categories_model import GeneralCategory  
from app.models.material_model import Material 
from app.models.industrial_model import IndustrialApplication

Material.generalcategoryid.property.columns[0].foreign_keys.clear()  
Material.generalcategoryid = db.Column(db.Integer, db.ForeignKey('generalcategories.GeneralCategoryID')) 

@pytest.fixture(scope="module")
def client():
    with app.app_context():
        db.create_all()

        inspector = inspect(db.engine)
        print(inspector.get_table_names())

        category_a = GeneralCategory(CategoryName='Category A')
        category_b = GeneralCategory(CategoryName='Category B')
        db.session.add(category_a)
        db.session.add(category_b)
        db.session.commit() 

        material_a = Material(materialname='Material A', generalcategoryid=category_a.GeneralCategoryID)
        material_b = Material(materialname='Material B', generalcategoryid=category_b.GeneralCategoryID)
        db.session.add(material_a)
        db.session.add(material_b)
        db.session.commit()

        application_a = IndustrialApplication(MaterialID=material_a.materialid, ApplicationName="App A", Industry="Industry A")
        application_b = IndustrialApplication(MaterialID=material_b.materialid, ApplicationName="App B", Industry="Industry B")
        db.session.add(application_a)
        db.session.add(application_b)
        db.session.commit()

        yield app.test_client()

        db.session.remove() 
        db.drop_all()  

@event.listens_for(Engine, "before_cursor_execute", retval=True)
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if "RETURNING" in statement and conn.dialect.name == "sqlite":
        new_statement = statement.replace(" RETURNING", "")
        return new_statement, params
    return statement, params

def test_get_industrial_applications_route(client):
    response = client.get('/api/industrial/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['application_name'] == "App A"
    assert data[1]['application_name'] == "App B"
