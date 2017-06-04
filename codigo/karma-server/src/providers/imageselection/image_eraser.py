''' Eraser of the EFES Algorithm '''
class ImageEraserAbstract:
    ''' Abstract class for the Eraser '''
    def erase(self, image_list, user_id):
        ''' Erase the images not valid for the user passed, returns the processed list '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def get_description(self):
        ''' Returns description for the implementation '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ImageEraser(ImageEraserAbstract):
    ''' Implementation of ImageEraserAbastract'''
    def erase(self, image_list, user_id):
        # TODO implement this
        return image_list

    def get_description(self):
        return 'Does nothing'
