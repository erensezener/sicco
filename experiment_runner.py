import functools
import traceback
import warnings
import time
from sicco import capturer, utils
from pprint import pprint
import shutil
import os
from functools import wraps


@utils.Singleton
class ExperimentRunner(object):
    def __init__(self, experiment=None, config_list=None):
        """
        Arguments:

        experiment: An object that inherits sicco.experiment.Experiment

        config_list: A list of objects that inherit sicco.config.Config
        """
        self.experiment = experiment
        self.config_list = config_list if config_list is not None else []
        self.log_list = []
        self.model_params_list = []

    def run(self):
        """
        Runs an experiment for each config in the config_list.
        """
        utils.debug_log('running an experiment', self.experiment.debug_mode)
        for i, config in enumerate(self.config_list):
            # experiment related data is stored in self.experiment
            std_output_list, warnings_list, exception_list, model_params = self._run_experiment(config)

            log = self._create_log_from_experiment_results(std_output_list, warnings_list, exception_list)
            self.log_list.append(log)

            self.model_params_list.append(model_params)
            utils.debug_log('config {} is complete'.format(i), self.experiment.debug_mode)

        utils.debug_log('running an experiment', self.experiment.debug_mode)

    def save(self):
        utils.debug_log('saving the results', self.experiment.debug_mode)
        utils.create_dir_if_it_does_not_exists(self.experiment.output_path)

        for i, (log, config, model_params) in enumerate(zip(self.log_list, self.config_list, self.model_params_list)):
            exp_results_dir_path = self.experiment.output_path + '/' + config.get_subdirectory_path
            utils.create_dir_if_it_does_not_exists(exp_results_dir_path)

            with open(exp_results_dir_path + '/config' + str(i) + '.out', 'wt') as out:
                pprint({'log': vars(log), 'config': vars(config)}, stream=out)

            utils.save_variables(exp_results_dir_path, model_params)
        self._copy_source_files(self.config_list[0].get_subdirectory_path)

    # TODO this function is ugly. Refactor.
    def _copy_source_files(self, destination_path):
        utils.debug_log('in _copy_source_files', self.experiment.debug_mode)

        if self.experiment.files_to_backup is None:
            pass
        else:
            extended_destination_path = self.experiment.output_path + '/' + destination_path + '/backup'

            if type(self.experiment.files_to_backup) is list:
                utils.create_dir_if_it_does_not_exists(extended_destination_path)
                for i, file in enumerate(self.experiment.files_to_backup):
                    if os.path.isdir(file):
                        shutil.copytree(file, extended_destination_path + '/' + str(i),
                                        ignore=lambda x, y: self.experiment.output_path)
                    elif os.path.isfile(file):
                        file_name_without_directory = file.split('/')[-1]
                        shutil.copyfile(file, extended_destination_path + '/' + file_name_without_directory)

            elif type(self.experiment.files_to_backup) is str:
                if os.path.isdir(self.experiment.files_to_backup):
                    shutil.copytree(self.experiment.files_to_backup, extended_destination_path,
                                    ignore=lambda x, y: self.experiment.output_path)

                elif os.path.isfile(self.experiment.files_to_backup):
                    file_name_without_directory = self.experiment.files_to_backup.split('/')[-1]
                    shutil.copyfile(self.experiment.files_to_backup,
                                    extended_destination_path + '/' + file_name_without_directory)

            else:
                raise RuntimeWarning('files_to_backup must be a string or a list of strings')

        utils.debug_log('exiting _copy_source_files', self.experiment.debug_mode)

    def _run_experiment(self, config):
        """
        Runs an experiment with a given config. Captures the warnings and std out writes.
        """
        exception = None
        std_output_list = []
        utils.debug_log('in _run_experiment', self.experiment.debug_mode)
        with warnings.catch_warnings(record=True) as warnings_list:
            try:
                with capturer.Capturing() as std_output_list:  # capture the stdout of an experiment
                    utils.debug_log('starting setting up', self.experiment.debug_mode)
                self.experiment.setup(config)
                utils.debug_log('finished setting up', self.experiment.debug_mode)
                utils.debug_log('starting running', self.experiment.debug_mode)
                self.experiment.run()
                utils.debug_log('finished running', self.experiment.debug_mode)
            except:
                exception = traceback.format_exc()
                print('Sicco handled an exception in {}'.format(config.description))

        utils.debug_log('exiting _run_experiment', self.experiment.debug_mode)
        return std_output_list, warnings_list, exception, self.experiment.get_model_params()

    def _create_log_from_experiment_results(self, std_output_list, warnings_list, exception_list):
        """
        Creates a Log object from the experiment outputs.
        """
        log = self.Log()
        log.exp_output = self.experiment.get_output()
        log.std_output = std_output_list
        log.method_runtimes = self.experiment.function_call_times
        log.warnings_list = [str(warning) for warning in warnings_list]
        log.exception_list = exception_list
        return log

    class Log:
        # def __init__(self):
        #     self.uid = utils.get_uuid_hex_string()

        def __str__(self):
            return str(vars(self))


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
        if func.__name__ not in self.function_call_times:
            self.function_call_times[func.__name__] = [elapsed_time]
        else:
            self.function_call_times[func.__name__].append(elapsed_time)

    return newfunc


def config(config_class):
    """
    Decorates a config class

    """
    config_object = config_class.__new__(config_class)
    config_object.__init__()
    runner = ExperimentRunner.Instance()
    runner.config_list.append(config_object)


def experiment(experiment_class=None, **options):
    """
    Decorates an experiment class, runs it and saves the parameters.
    The Experiment class comes with 4 abstract methods that need to be overriden.
    Make sure to check the Experiment class to see those methods.

    Optional arguments:

    output_path: string, default='./sicco_logs'
        The path in which sicco outputs will be stored.

    files_to_backup: string or [string], default='.'
        A path or a list of paths that points to files or directories to be backed up.

    debug_mode: boolean, default=False
        Sicco is verbose if debug_mode is True. This is for development purposes.

    """
    if experiment_class is not None:
        experiment_class = experiment_class
        experiment_object = experiment_class.__new__(experiment_class)
        experiment_object.__init__(**options)
        runner = ExperimentRunner.Instance()
        runner.experiment = experiment_object
        runner.run()
        runner.save()

    else:
        @functools.wraps(experiment)
        def wrapper(cls):
            return experiment(cls, **options)

        return wrapper
