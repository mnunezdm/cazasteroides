''' Puntuation module '''
from colorama import Fore
from models import db

# class Puntuation:
class Puntuation(db.Model):
    observation_id = db.Column(db.Integer, db.ForeignKey('observation.observation_id'), primary_key=True)
    positive = db.Column(db.Integer)
    negative = db.Column(db.Integer)
    ''' Puntuation class '''
    def __init__(self, votes):
        self.positive = votes.upvotes
        self.negative = votes.downvotes

    def __str__(self):
        parse = Fore.GREEN + '+' + str(self.positive) + Fore.RED + ' -' + str(self.negative)
        parse = parse + Fore.RESET + ' ({}%)'.format(self.calculate_certainty()*100)
        string = Fore.GREEN + '+' + str(self.positive) + Fore.RED + ' -'
        string = string + str(self.negative) + Fore.RESET
        return string

    def serialize(self):
        ''' Serializes object '''
        return {
            "positive": self.positive,
            "negative": self.negative,
            "certainty": self.calculate_certainty()
        }

    def add_vote(self, vote_type, karma_level):
        ''' Adds a new vote, returns the certainty '''
        if vote_type:
            self.positive = self.positive + karma_level
        else:
            self.negative = self.negative + karma_level
        return self.calculate_certainty()

    def calculate_certainty(self):
        ''' Calculates the certainty '''
        try:
            return (self.positive - self.negative) / (self.positive + self.negative)
        except ZeroDivisionError:
            return 0
