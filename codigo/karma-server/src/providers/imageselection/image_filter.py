''' Filter of the EFES Algorithm '''
class ImageFilterAbstract:
    ''' Abstract class for Image Filter '''
    def filter(self, images_list, karma_level, number_of_levels):
        ''' Filter the images passed '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

    def get_images_for_level(self, karma_level):
        ''' Gets the images for the karma level passed '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ImageFilter(ImageFilterAbstract):
    ''' Implementation of the Filter class '''
    def filter(self, images_list, karma_level, number_of_levels):
        # TODO implement this
        raise NotImplementedError('Not implemented... yet...')

    def get_images_for_level(self, karma_level):
        # TODO implement this
        raise NotImplementedError('Not implemented... yet...')
        