''' Puntuation module '''
from colorama import Fore
from karmaserver.data.models import db


class Puntuation(db.Model):
    ''' Puntuation class implementation '''
    observation_id = db.Column(db.String(64), db.ForeignKey('observation._id'), primary_key=True)
    positive = db.Column(db.Integer)
    negative = db.Column(db.Integer)
    ''' Puntuation class '''
    def __init__(self, votes):
        self.positive = votes.upvotes
        self.negative = votes.downvotes

    def __str__(self):
        positive = Fore.GREEN + '+' + str(self.positive) + Fore.RESET
        negative = Fore.RED + '-' + str(self.negative) + Fore.RESET
        return f'{positive}\t{negative}\t{self.calculate_certainty()*100}%'

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
