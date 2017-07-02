''' Eraser of the EFES Algorithm '''
class ObservationEraserAbstract:
    ''' Abstract class for the Eraser '''
    def erase(self, observation_list, user_id):
        ''' Erase the observations not valid for the user passed, returns the processed list '''
        raise NotImplementedError('Abstract class, this method should have been implemented')


class ObservationEraser(ObservationEraserAbstract):
    ''' Implementation of ObservationEraserAbastract, erases every repeated observation '''
    def erase(self, observation_list, user_id):
        return [observation for observation in observation_list
                if user_id not in observation.users_who_voted]
