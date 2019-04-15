''' Observation module '''
from enum import Enum

from colorama import Fore

from karmaserver.data.models import db, user_observations
from karmaserver.data.models.position import Position
from karmaserver.data.models.puntuation import Puntuation
from karmaserver.data.models.votes import Votes
from karmaserver.utils.print import DATA_TAG, info, to_string_list


class State(Enum):
    ''' Enum class for states, observations can be in 3 states,
    DENYED, APPROVED or PENDING (default) '''
    DENYED = 'denyed'
    APPROVED = 'approved'
    PENDING = 'pending'
    DISPUTED = 'disputed'


class ObservationAbstract: # pragma: no cover
    ''' Abstract class for Observations '''
    def add_vote(self, vote_info, user):
        ''' Inserts the new vote and returns the new number of votes and the certainty '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def change_state(self, change_to):
        ''' Changes the state of the observation and notifies the Astronomer '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def get_notified(self):
        ''' Returns if the Astronomer has been notified '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def serialize(self, only_id=False, difficulty=False, id_position=False):
        ''' Serializes the object, has two modes:\n
        only_id = True => serializes only the id\n
        only_id = False => serializes all the object'''
        raise NotImplementedError('Abstract class, this method should have been implemented')


class Observation(ObservationAbstract, db.Model):
    ''' Implementation of the Observation '''
    _id = db.Column(db.String(64), primary_key=True)
    state = db.Column(db.Enum(State))

    image_id = db.Column(db.String(64), db.ForeignKey('image._id'))
    votes = db.relationship('Votes', uselist=False, lazy='joined')
    position = db.relationship('Position', uselist=False, lazy='joined')
    puntuation = db.relationship('Puntuation', uselist=False, lazy='joined')

    users_who_voted = db.relationship('User', secondary=user_observations, lazy='joined')

    brightness = db.Column(db.Integer)

    def __init__(self, observation_info):
        self._id = observation_info['_id']
        self.image_id = observation_info['image']['_id']
        self.brightness = observation_info['brightness']

        self.votes = Votes(observation_info['votes'])
        self.position = Position(observation_info['position'])
        self.puntuation = Puntuation(self.votes)

        self.difficulty = -1
        self.certainty = 0

        self.state = State.PENDING

    def __str__(self):
        parse = DATA_TAG + f' Observation (id={self._id})\n'
        parse = parse + to_string_list('votes', self.votes)
        parse = parse + to_string_list('puntuation', self.puntuation)
        parse = parse + to_string_list('position', self.position)
        parse = parse + to_string_list('state', self.state)
        return parse

    def __eq__(self, observation):
        return observation == self._id

    def __repr__(self): # pragma: no cover
        return f'<{Observation.__name__}, {self._id}, {self.puntuation.calculate_certainty()}>'

    def serialize(self, only_id=False, difficulty=False, id_position=False): # pragma: no cover
        ''' Serializes the object, has two modes:\n
        only_id = True => serializes only the id\n
        only_id = False => serializes all the object'''
        if only_id:
            return {"_id": self._id}
        if id_position:
            return {
                "observation_id": self._id,
                "image_id": self.image_id,
                "state": self.state.value,
                "position": self.position.serialize()
            }
        if difficulty:
            return {
                "_id": self._id,
                "difficulty": self.difficulty
            }
        return {
            "_id": self._id,
            "image_id": self.image_id,
            "votes": self.votes.serialize(),
            "puntuation": self.puntuation.serialize(),
            "position": self.position.serialize(),
            "state": self.state.value,
            "users_who_voted": [user.get_id() for user in self.users_who_voted]
            }

    def add_vote(self, vote_info, user):
        vote_type = vote_info['vote_type']
        karma_level = vote_info['karma_level']

        number_of_votes = self.votes.add_vote(vote_type)
        certainty = self.puntuation.add_vote(vote_type, karma_level)
        self.users_who_voted.append(user)
        return number_of_votes, certainty

    def change_state(self, change_to):
        ''' Changes the state of the observation based on the approved parameter\n
        approved=True => approved \n approved=False => denyed '''
        if self.state != change_to:
            self.state = change_to
            colored_state = f'{Fore.CYAN}\'{self.state.value}\'{Fore.RESET}'
            info(f'OBSER', f'{self._id} state changed to {colored_state}')

    def get_notified(self):
        ''' Returns if this observation has  '''
        return State.APPROVED == self.state or State.DENYED == self.state

    def repeated_vote(self, user):
        ''' Detects if the user passed has already voted this observation '''
        for user_who_voted in self.users_who_voted:
            if user == user_who_voted:
                return True

    def get_certainty(self):
        ''' Calculates the certainty of this image '''
        if self.get_certainty:
            return self.get_certainty
        return self.puntuation.get_certainty()

    def user_has_voted(self, current_user):
        ''' Detects if the user passed has already voted '''
        for user in self.users_who_voted:
            if user == current_user:
                return True
