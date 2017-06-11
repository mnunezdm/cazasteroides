''' Selector of the EFES Algorithm '''
import operator

class ImageSelectorAbstract:
    ''' Abstract class for the Selector '''
    def select(self, observation_list):
        ''' Select an image from the list '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ImageSelector(ImageSelectorAbstract):
    ''' Implementation of ImageSelectorAbastract'''
    def select(self, observation_list):
        sorted_list = self.__sort(observation_list)
        if sorted_list:
            return observation_list[0]

    @staticmethod
    def __sort(image_list):
        return sorted(image_list, key=lambda x: x.puntuation.calculate_certainty(), reverse=True)
