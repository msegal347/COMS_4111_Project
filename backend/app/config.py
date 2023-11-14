import os

class Config(object):
    # Flask settings
    FLASK_DEBUG = bool(os.environ.get("FLASK_DEBUG", False))

    # PostgreSQL settings
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "materials")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "materials")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "materialsDB")
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")

    # Construct the PostgreSQL URL
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # Secret key for session management
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret")

    # CORS settings
    CORS_HEADERS = os.environ.get("CORS_HEADERS", "*")

