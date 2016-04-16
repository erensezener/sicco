from functools import wraps
from abc import ABCMeta, abstractmethod

import time


class Experiment(metaclass=ABCMeta):
    def __init__(self):
        self.function_call_times = {}

    @abstractmethod
    def setup(self, config):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def get_output(self):
        pass


def timeit(func):
    """
    This is a decorator for timing arbitrary methods.
    """

    @wraps(func)
    def newfunc(*args, **kwargs):
        print('Dec called')

        self = args[0]

        start_time = time.time()
        func(*args, **kwargs)
        elapsed_time = time.time() - start_time

        self.function_call_times[func.__name__] = elapsed_time

    return newfunc
