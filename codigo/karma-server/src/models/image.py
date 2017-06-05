''' Image module '''
from models import db

class Image(db.Model):
    ''' Image class
    ATTENTION!!! If migrate doesnt detect this class, move it to the __init__.py of this package '''
    image_id = db.Column(db.Integer, primary_key=True)
    observations = db.relationship('Observation', backref='image', lazy='joined')
    probability = db.Column(db.Integer)
    fwhm = db.Column(db.Integer)

    def __init__(self, image_id):
        self.image_id = image_id
        self.observations = []
        self.probability = 0
        self.fwhm = 0
