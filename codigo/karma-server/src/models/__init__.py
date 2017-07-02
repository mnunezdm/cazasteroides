''' Models module '''
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


user_observations = (
    db.Table('user_observations',
             db.Column('observation_id', db.String(64), db.ForeignKey('observation._id')),
             db.Column('user_id', db.String(64), db.ForeignKey('user._id'))
            )
    )
