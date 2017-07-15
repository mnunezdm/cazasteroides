''' Votes Module '''
from colorama import Fore
from data.models import db


class Votes(db.Model):
    observation_id = db.Column(db.String(64), db.ForeignKey('observation._id'),
                               primary_key=True)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)

    ''' Votes class '''
    def __init__(self, json):
        self.upvotes = json['upvotes']
        self.downvotes = json['downvotes']

    def __str__(self):
        positive = Fore.GREEN + '+' + str(self.upvotes) + Fore.RESET
        negative = Fore.RED + '-' + str(self.downvotes) + Fore.RESET
        return f'{positive}\t{negative}'

    def add_vote(self, vote_type):
        ''' Adds a new vote, returns the number of votes '''
        if vote_type:
            self.upvotes = self.upvotes + 1
        else:
            self.downvotes = self.downvotes + 1
        return self.number_of_votes()

    def number_of_votes(self):
        ''' Returns the number of votes '''
        return self.upvotes + self.downvotes

    def serialize(self):
        ''' Serializes object '''
        return {
            "upvotes": self.upvotes,
            "downvotes": self.downvotes
        }
