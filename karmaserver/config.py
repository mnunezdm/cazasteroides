''' Configuration Params for Flask Server '''
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

ENDPOINT = 'http://localhost:5000'

# Level Default Values
DEFAULT_FORMULA = 'math.log ( ( level / 3 ) + 1 ) * 350'
MAX_KARMA_LEVEL = 10
# Validation Values
MINIMUM_VOTES = 6
VOTES_TO_DISPUTED = 10
VOTES_TO_MINIMUM_CERTAINTY = VOTES_TO_DISPUTED * 3
CERTAINTY_UPPER_LIMIT = 0.75
CERTAINTY_LOWER_LIMIT = 0.45
# Filter Module Values
MAX_FILTER_LEVEL = 5
