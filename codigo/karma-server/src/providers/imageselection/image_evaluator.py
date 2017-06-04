''' Evaluator of the EFES Algorithm '''
class ImageEvaluatorAbstract:
    ''' Abstract class for Image Evaluator '''
    def evaluate(self, images_list, observation_list):
        ''' Evaluate the images passed '''
        raise NotImplementedError('Abstract class, this method should have been implemented')

class ImageEvaluator(ImageEvaluatorAbstract):
    ''' Implementation of the Evaluator class '''
    def evaluate(self, images_list, observation_list):
        observation_list = []
        for image in images_list:
            observation_for_image = image.get_observations(observation_list)
            self.__evaluate_image(images_list, observation_for_image)

    def __evaluate_image(self, image, observation_for_image):
        probability = image.probability
        fwhm = image.fwhm
        observations_value = self.__observations_value(observation_for_image)
        return probability + fwhm + observations_value

    def __observations_value(self, observations):
        value = 0
        for observation in observations:
            value = value + observation.get_value(observation)
        return value
        