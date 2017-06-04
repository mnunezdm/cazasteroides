''' EFES Provider module '''
from providers.imageselection.image_evaluator import ImageEvaluator
from providers.imageselection.image_filter import ImageFilter
from providers.imageselection.image_eraser import ImageEraser
from providers.imageselection.image_selector import ImageSelector
from debugger import print_info

class ImageSelectionProviderAbstract:
    ''' Abstract class of the EFES Provider class '''
    def get_image(self, user_id, karma_level):
        ''' Returns the image based on the karma_level and the user_id '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ImageSelectionProvider(ImageSelectionProviderAbstract):
    ''' Implementation of the EFES Provider class '''
    def __init__(self):
        print_info('INFO', 'Initializing Image Selection Provider')
        self.evaluator = ImageEvaluator()
        self.filter = ImageFilter()
        self.eraser = ImageEraser()
        self.selector = ImageSelector()
        images = self.__get_images()
        observations = self.__get_observations()
        self.images = self.evaluator.evaluate(images, observations)

    @staticmethod
    def __get_images():
        # TODO Get Images from somewhere
        return {}

    @staticmethod
    def __get_observations():
        # TODO Get Images from somewhere
        return {}

    def get_image(self, user_id, karma_level):
        filtered_images = self.filter.get_images_for_level(karma_level)
        erased_images = self.eraser.erase(filtered_images, user_id)
        selected_image = self.selector.select(erased_images)
        return selected_image
        