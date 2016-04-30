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
