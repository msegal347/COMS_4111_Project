import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, event
from sqlalchemy.engine import Engine

# Create a new SQLAlchemy object
db = SQLAlchemy()

# Create a new Flask app instance for testing
def create_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost.local'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

app = create_app()

# Ensure all models are imported here
from app.models.general_categories_model import GeneralCategory  # Import the GeneralCategory model
from app.models.material_model import Material  # Make sure this import is correct
from app.models.industrial_model import IndustrialApplication

# Correct the Material model's ForeignKey reference before setting up the test client
Material.generalcategoryid.property.columns[0].foreign_keys.clear()  # Clear existing foreign key
Material.generalcategoryid = db.Column(db.Integer, db.ForeignKey('generalcategories.GeneralCategoryID'))  # Set correct foreign key

# Fixture for creating the test client and setting up the database
@pytest.fixture(scope="module")
def client():
    with app.app_context():
        # Create tables for each model
        db.create_all()

        # Now, we can inspect the tables to ensure creation
        inspector = inspect(db.engine)
        print(inspector.get_table_names())

        # Setup data for testing
        # First, create an instance of GeneralCategory
        category_a = GeneralCategory(CategoryName='Category A')
        category_b = GeneralCategory(CategoryName='Category B')
        db.session.add(category_a)
        db.session.add(category_b)
        db.session.commit()  # Commit to assign IDs

        # Create instances of Material that reference the GeneralCategory
        material_a = Material(materialname='Material A', generalcategoryid=category_a.GeneralCategoryID)
        material_b = Material(materialname='Material B', generalcategoryid=category_b.GeneralCategoryID)
        db.session.add(material_a)
        db.session.add(material_b)
        db.session.commit()  # Commit to assign IDs

        # Create instances of IndustrialApplication that reference Material
        application_a = IndustrialApplication(MaterialID=material_a.materialid, ApplicationName="App A", Industry="Industry A")
        application_b = IndustrialApplication(MaterialID=material_b.materialid, ApplicationName="App B", Industry="Industry B")
        db.session.add(application_a)
        db.session.add(application_b)
        db.session.commit()

        yield app.test_client()  # Provides the test client for the tests

        db.session.remove()  # Close the session to avoid hanging transactions
        db.drop_all()  # Clean up the tables after tests

@event.listens_for(Engine, "before_cursor_execute", retval=True)
def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
    if "RETURNING" in statement and conn.dialect.name == "sqlite":
        # Modify the statement to remove the RETURNING clause
        new_statement = statement.replace(" RETURNING", "")
        return new_statement, params
    return statement, params

# Test function for GET route to fetch all industrial applications
def test_get_industrial_applications_route(client):
    response = client.get('/api/industrial/')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['application_name'] == "App A"
    assert data[1]['application_name'] == "App B"
