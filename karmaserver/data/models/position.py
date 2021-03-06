''' Position module '''
from random import random
from karmaserver.data.models import db


class Position(db.Model):
    ''' Observation Position implementation '''
    observation_id = db.Column(db.String(64), db.ForeignKey('observation._id'),
                               primary_key=True)
    x_position = db.Column(db.Integer)
    y_position = db.Column(db.Integer)

    ''' Position Class '''
    def __init__(self, positon_data=None, x_position=0, y_position=0):
        # if positon_data:
        self.x_position = positon_data['x']
        self.y_position = positon_data['y']
        # else:
        #     self.x_position = x_position
        #     self.y_position = y_position

    def __str__(self): # pragma: no cover
        return f'x:{self.x_position}\ty:{self.y_position}'

    def serialize(self): # pragma: no cover
        ''' Serializes object '''
        return {
            "x": self.x_position,
            "y": self.y_position
            }

    # def create_random_position(self, max_x_offset, max_y_offset):
    #     ''' Creates a position in which the position of this object is inside of the
    #     rectable built with offsets passed as parameter, for sending the new image '''
    #     new_x = self.__calculate_random_axis(max_x_offset, self.x_position)
    #     new_y = self.__calculate_random_axis(max_y_offset, self.y_position)
    #     return Position(x_position=new_x, y_position=new_y)

    # @staticmethod
    # def __calculate_random_axis(max_offset, axis_position):
    #     offset = random() * max_offset
    #     new_position = axis_position - offset
    #     return 0 if new_position < 0 else new_position
        