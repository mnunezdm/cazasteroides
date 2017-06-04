''' Observation module '''
from debugger import DATA_TAG, to_string_list
from models.position import Position
from models.puntuation import Puntuation
from models.votes import Votes
from models import db, user_observations, User

# class ObservationAbstract(db.Model):
class ObservationAbstract:
    ''' Abstract class for Observations '''
    def add_vote(self, vote_info):
        ''' Inserts the new vote, also, returns the new number of votes and the certainty '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def change_state(self, to_approved):
        ''' Changes the state of the observation and notifies the Astronomer '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def get_notified(self):
        ''' Returns if the Astronomer has been notified '''
        raise NotImplementedError('Abstract class, this method should have been implemented')
    def serialize(self):
        ''' Serializes the observation '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def get_value(self):
        ''' Gets the value for the observation '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

# class Observation(ObservationAbstract):
class Observation(ObservationAbstract, db.Model):
    ''' Implementation of the Observation '''
    observation_id = db.Column(db.String(64), primary_key=True)
    state = db.Column(db.String(16))
    image_id = db.Column(db.String(64), db.ForeignKey('image.image_id'))

    votes = db.relationship('Votes', uselist=False, lazy='joined')
    position = db.relationship('Position', uselist=False, lazy='joined')    
    puntuation = db.relationship('Puntuation', uselist=False, lazy='joined')

    users_who_voted = db.relationship('User', secondary=user_observations,
                                      backref='Observation')

    def __init__(self, observation_info):
        self.observation_id = observation_info['observation_id']
        self.image_id = observation_info['image_id']

        self.votes = Votes(observation_info['votes'])
        self.position = Position(observation_info['position'])
        self.puntuation = Puntuation(self.votes)

        self.users_who_voted = []
        self.state = 'pending'

    def __str__(self):
        parse = DATA_TAG + ' Observation ({})\n'.format(self.observation_id)
        parse = parse + to_string_list('votes', self.votes)
        parse = parse + to_string_list('puntuation', self.puntuation)
        parse = parse + to_string_list('position', self.position)
        parse = parse + to_string_list('state', self.state)
        return parse

    def serialize(self):
        return {
            "observation_id": self.observation_id,
            "image_id": self.image_id,
            "votes": self.votes.serialize(),
            "puntuation": self.puntuation.serialize(),
            "position": self.position.serialize(),
            "state": self.state,
            }

    def add_vote(self, vote_info):
        vote_type = vote_info['vote_type']
        karma_level = vote_info['karma_level']
        number_of_votes = self.votes.add_vote(vote_type)
        certainty = self.puntuation.add_vote(vote_type, karma_level)
        user = User(vote_info['user_id']) # TODO check before insert
        self.users_who_voted.append(user)
        return number_of_votes, certainty

    def change_state(self, to_approved):
        self.state = 'approved' if to_approved else 'denyed'

    def get_notified(self):
        return 'pending' not in self.state

    def get_value(self):
        number_of_votes = self.votes.number_of_votes()
        multiplier = self.__get_multiplier()
        return number_of_votes * multiplier

    def __get_multiplier(self): # TODO implement an enum?
        if 'approved' in self.state:
            return 1
        if 'pending' in self.state:
            return 0.5
        if 'denyed' in self.state:
            return 0.10
    
    def update_in_database(self):
        db.session.add(self)
        db.session.commit()

def get_observation_or_create_it(observation_info):
    observation_id = observation_info['observation_id']
    observation = get_observation(observation_id)
    if not observation:
        observation = Observation(observation_info)
    return observation

def get_observation(observation_id):
    return db.session.query(Observation).filter(observation_id).first()
