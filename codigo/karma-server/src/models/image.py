''' Image module '''
from models import db

class Image(db.Model):
    ''' Image class '''
    _id = db.Column(db.Integer, primary_key=True)
    observations = db.relationship('Observation', backref='image', lazy='joined')
    x_size = db.Column(db.Integer)
    y_size = db.Column(db.Integer)
    probability = db.Column(db.Integer)
    fwhm = db.Column(db.Integer)

    def __init__(self, _id, x_size, y_size):
        self._id = _id
        self.x_size = x_size
        self.y_size = y_size
        self.probability = 0
        self.fwhm = 0
