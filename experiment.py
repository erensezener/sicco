from functools import wraps
from abc import ABCMeta, abstractmethod
from sicco import utils
import time


class Experiment(metaclass=ABCMeta):
    def __init__(self):
        self.function_call_times = {}
        self.uid = utils.get_uuid_hex_string()

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


# TODO check if args[0] is an instance of Experiment
def timeit(func):
    """
    This is a decorator for capturing the runtime of arbitrary methods.
    """
    @wraps(func)
    def newfunc(*args, **kwargs):
        self = args[0]
        start_time = time.time()
        func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        self.function_call_times[func.__name__] = elapsed_time

    return newfunc
