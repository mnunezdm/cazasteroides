from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_observations = (
    db.Table('user_observations',
             db.Column('observation_id', db.String(64), db.ForeignKey('observation.observation_id')),
             db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')))
    )
