''' Configuration Params for Flask Server '''
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

ENDPOINT = 'http://localhost:5000/'

# Server Default Values

MAX_KARMA_LEVEL = 10
POINTS_PER_OBSERVATION = 100

MINIMUM_VOTES = 10
MAXIMUM_VOTES = 20
LOWER_LIMIT = -0.75
UPPER_LIMIT = 0.75

MAX_FILTER_LEVEL = 5
