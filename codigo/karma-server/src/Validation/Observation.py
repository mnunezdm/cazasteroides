''' Observation module '''

from colorama import Fore

class ObservationAbstract:
    ''' Abstract class for Observations '''

    def add_vote(self, karma_level, vote_type):
        ''' Inserts the new vote, also, returns the new number of votes and the certainty '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def change_state(self, to_approved):
        ''' Changes the state of the observation and notifies the Astronomer '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def get_notified(self):
        ''' Returns if the Astronomer has been notified '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def update_observation_in_db(self):
        ''' Updates the db with the new data '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def serialize(self):
        ''' Serializes the observation '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class Observation(ObservationAbstract):
    ''' Implementation of the Observation '''
    def __init__(self, observation_id, upvotes, downvotes, database=None):
        self.observation_id = observation_id
        self.upvotes = upvotes
        self.downvotes = downvotes
        self.positive_puntuation = upvotes
        self.negative_puntuation = downvotes
        self.database = database
        self.state = 'pending'

    def __str__(self):
        parse = Fore.CYAN + '[DATA]' + Fore.RESET + ' Observation ({})'.format(self.observation_id)
        parse = parse + '\n\t- ' + Fore.CYAN + 'votes' + Fore.RESET + ':\t' + Fore.GREEN + '+'
        parse = parse + str(self.upvotes) + Fore.RED + ' -' + str(self.downvotes) + Fore.RESET
        parse = parse + '\n\t- ' + Fore.CYAN + 'puntuation' + Fore.RESET + ':\t'  + Fore.GREEN
        parse = parse + '+' + str(self.positive_puntuation) + Fore.RED + ' -' + str(self.downvotes)
        parse = parse + Fore.RESET + ' ({}%)'.format(self.__calculate_certainty()*100) + "\n\t- "
        parse = parse + Fore.CYAN + 'notified' + Fore.RESET + ':\t' + self.state
        return parse

    def serialize(self):
        return {"_id": self.observation_id,
                "upvotes": self.upvotes,
                "downvotes": self.downvotes,
                "positive_puntuation": self.positive_puntuation,
                "negative_puntuation": self.negative_puntuation,
                "state": self.state,
                "certainty": self.__calculate_certainty()
               }

    def add_vote(self, karma_level, vote_type):
        if vote_type:
            self.positive_puntuation = self.positive_puntuation + karma_level
            self.upvotes = self.upvotes + 1
        else:
            self.negative_puntuation = self.negative_puntuation + karma_level
            self.downvotes = self.downvotes + 1
        return self.__number_of_votes(), self.__calculate_certainty()

    def __calculate_certainty(self):
        try:
            return (self.positive_puntuation - self.negative_puntuation) / (
                self.positive_puntuation + self.negative_puntuation)
        except ZeroDivisionError:
            return 0

    def __number_of_votes(self):
        return self.upvotes + self.downvotes

    def change_state(self, to_approved):
        self.state = 'approved' if to_approved else 'denyed'

    def get_notified(self):
        return 'pending' not in self.state

    def update_observation_in_db(self):
        pass # TODO update DB
