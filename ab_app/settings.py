import os

from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('BASE_URL')

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')

SPATIALITE_LIBRARY_PATH = os.getenv('SPATIALITE_LIBRARY_PATH')

