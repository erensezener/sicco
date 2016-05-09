from abc import ABCMeta, abstractmethod
from sicco import utils


class Experiment(metaclass=ABCMeta):
    def __init__(self, output_path='./sicco_logs', files_to_backup='.', debug_mode=False):
        self.function_call_times = {}
        self.uid = utils.get_uuid_hex_string()
        self.output_path = output_path
        self.files_to_backup = files_to_backup
        self.debug_mode = debug_mode

    @abstractmethod
    def setup(self, config):
        raise NotImplementedError('The abstract methods in Experiment should be overriden')

    @abstractmethod
    def run(self):
        raise NotImplementedError('The abstract methods in Experiment should be overriden')

    @abstractmethod
    def get_output(self):
        raise NotImplementedError('The abstract methods in Experiment should be overriden')

    @abstractmethod
    def get_model_params(self):
        raise NotImplementedError('The abstract methods in Experiment should be overriden')



