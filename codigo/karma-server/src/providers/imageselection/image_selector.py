''' Selector of the EFES Algorithm '''
import operator

class ImageSelectorAbstract:
    ''' Abstract class for the Selector '''
    def select(self, image_list):
        ''' Select an image from the list '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ImageSelector(ImageSelectorAbstract):
    ''' Implementation of ImageSelectorAbastract'''
    def select(self, image_list):
        sorted_list = self.__sort(image_list)
        if sorted_list:
            return image_list[0]

    @staticmethod
    def __sort(image_list):
        return sorted(image_list, key=operator.itemgetter('difficulty'))
