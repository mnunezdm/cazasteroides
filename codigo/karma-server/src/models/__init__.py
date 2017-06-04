from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_observations = (
    db.Table('user_observations',
             db.Column('observation_id', db.String(64), db.ForeignKey('observation.observation_id')),
             db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')))
    )

class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    observations = db.relationship('Observation', backref='image', lazy='joined')
    probability = db.Column(db.Integer)
    fwhm = db.Column(db.Integer)

    def __init__(self, image_id):
        self.image_id = image_id
        self.observations = []
        self.probability = 0
        self.fwhm = 0

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    observations = db.relationship('Observation', secondary=user_observations,
                                   backref='User')
    def __init__(self, user_id):
        self.user_id = user_id
