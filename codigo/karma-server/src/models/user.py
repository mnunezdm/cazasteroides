''' module for user class '''
from models import db, user_observations
class User(db.Model):
    ''' User class '''
    _id = db.Column(db.Integer, primary_key=True)
    observations = db.relationship('Observation', secondary=user_observations, backref='User')

    def __init__(self, user_info):
        self._id = user_info['_id']

    def __str__(self):
        return str(self._id)

    def __eq__(self, user):
        if isinstance(user, User):
            return self._id is user._id
        if isinstance(user, str):
            return user == str(self._id)

    def serialize(self, only_id=True):
        ''' Serializes the object, has two modes:\n
        only_id = True => serializes only the id\n
        only_id = False => serializes id + observations'''
        if only_id:
            return {
                "_id": self._id
            }
        return {
            "_id": self._id,
            'observations': [observation.serialize(only_id=True)
                             for observation in self.observations]
        }
