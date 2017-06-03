''' Observation module '''
from debugger import to_string_list, DATA_TAG
from models.position import Position
from models.puntuation import Puntuation
from models.votes import Votes

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

class Observation(ObservationAbstract):
    ''' Implementation of the Observation '''
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
        self.users_who_voted.append(vote_info['user_id'])
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
