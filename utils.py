import os
import time
import uuid
import numpy as np
import pickle
from sklearn.externals import joblib


def create_dir_if_it_does_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_time_date_string():
    return time.strftime("%d-%m-%Y_%H:%M:%S")


def get_uuid_hex_string():
    return uuid.uuid4().hex


def debug_log(log_text, debug_mode):
    if debug_mode:
        print('sicco: ' + log_text)


def save_variables(log_path, variable_dict):
    """
    Saves variables (only meant for classes and numpy arrays).
    Pickles objects and uses joblib dump for numpy arrays

    :param log_path: the folder name for the logs
    :param variable_dict: a dictionary consisting of {var_name: var}
            where var_name is a string that denotes what the variable to be saved is

    Example:
    a = np.array([1,2,3])
    save_variables('.', {'a': a})

    """

    create_dir_if_it_does_not_exists(log_path)

    for var_name, var in variable_dict.items():
        if isinstance(var, np.ndarray):
            try:
                joblib.dump(var, log_path + '/' + var_name + '.jl')
            except:
                raise RuntimeWarning('Joblib dump failed in save_variables()')
        else:
            try:
                pickle.dump(var, open(log_path + '/' + var_name + '.pkl', "wb"))
            except:
                raise RuntimeWarning('Pickle dump failed in save_variables()')


class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    This code is shamelessly taken from:
    http://stackoverflow.com/questions/31875/is-there-a-simple-elegant-way-to-define-singletons-in-python

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
