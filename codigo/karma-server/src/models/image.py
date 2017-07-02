''' Image module '''
from models import db


class Image(db.Model):
    ''' Image class '''
    _id = db.Column(db.String(64), primary_key=True)
    observations = db.relationship('Observation', backref=db.backref('image', lazy='joined'))
    x_size = db.Column(db.Integer)
    y_size = db.Column(db.Integer)
    probability = db.Column(db.Integer)
    fwhm = db.Column(db.Integer)

    def __init__(self, image_info):
        self.observations = []
        self._id = image_info['_id']
        self.x_size = image_info['x_size']
        self.y_size = image_info['y_size']
        self.probability = image_info['probability']
        self.fwhm = image_info['fwhm']

    def __eq__(self, image):
        return image == self._id
        