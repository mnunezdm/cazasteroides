''' Eraser of the EFES Algorithm '''
class ImageEraserAbstract:
    ''' Abstract class for the Eraser '''
    def erase(self, observation_list, user_id):
        ''' Erase the images not valid for the user passed, returns the processed list '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ImageEraser(ImageEraserAbstract):
    ''' Implementation of ImageEraserAbastract, erases every repeated observation '''
    def erase(self, observation_list, user_id):
        processed_list = [observation for observation in observation_list
                          if str(user_id) not in observation.users_who_voted]
        print('processed', processed_list, len(processed_list))
        return processed_list
