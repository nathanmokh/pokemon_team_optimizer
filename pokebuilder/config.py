import os


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRESQL_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
