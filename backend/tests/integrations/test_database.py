from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

DATABASE_URI = 'postgresql://materials:materials@localhost:5432/materialsDB'

def test_connection(uri):
    try:
        engine = create_engine(uri)
        with engine.connect() as connection:
            # Use the text() function to create a SQL expression text clause
            result = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
            tables = [row[0] for row in result]
            return tables
    except OperationalError as e:
        return f"Error: {e}"

if __name__ == "__main__":
    tables = test_connection(DATABASE_URI)
    print(f"Tables in the database: {tables}")
