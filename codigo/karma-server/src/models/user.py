''' module for user class '''
from models import db, user_observations
class User(db.Model):
    ''' User class
    ATTENTION!!! If migrate doesnt detect this class, move it to the __init__.py of this package '''
    user_id = db.Column(db.Integer, primary_key=True)
    observations = db.relationship('Observation', secondary=user_observations,
                                   backref='User')
    def __init__(self, user_id):
        self.user_id = user_id
