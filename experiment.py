from abc import ABCMeta, abstractmethod
from sicco import utils


class Experiment(metaclass=ABCMeta):
    """
    This is an abstract class that has 4 methods that need to be overriden.
    Please do not edit this class.

    """
    def __init__(self, output_path='./sicco_logs', files_to_backup='.', debug_mode=False):
        self.function_call_times = {}
        self.uid = utils.get_uuid_hex_string()
        self.output_path = output_path
        self.files_to_backup = files_to_backup
        self.debug_mode = debug_mode

    @abstractmethod
    def setup(self, config):
        """
        All setting up related things should be done here. All the meta-parameters of the classifier
        should be defined in sicco.config.Config.

        Arguments:

        config: An object of a class that overrides sicco.config.Config

        """
        raise NotImplementedError('The abstract methods in Experiment should be overriden')

    @abstractmethod
    def run(self):
        """
        Heavy computation should be done here.
        """
        raise NotImplementedError('The abstract methods in Experiment should be overriden')

    @abstractmethod
    def get_output(self):
        """
        This enables the results of an experiment to be stored in a text file.

        The results of the experiment should be stored in a dictionary such that
                dict key: a string that explains what the variable is
                dict value: array-like (numpy arrays or lists etc.)

        Examples:
            return {'accuracies': self.accuracies, 'f-scores': self.f_scores}
        """
        raise NotImplementedError('The abstract methods in Experiment should be overriden')

    @abstractmethod
    def get_model_params(self):
        """
        This enables saving all the model related objects.

        The results of the experiment should be stored in a dictionary such that
                dict key: a string that explains what the objects is
                dict value: arbitrary data structure

        Examples:
            return {'classifier': self.clf, 'best lambda': self.best_lambda}
        """

        raise NotImplementedError('The abstract methods in Experiment should be overriden')



