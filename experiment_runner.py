import warnings
import capturer
import utils
from pprint import pprint
import shutil
import os


class ExperimentRunner(object):
    def __init__(self, experiment, config_list, output_path='./sicco_logs', files_to_backup='.'):
        """
        :param experiment: An object that inherits Experiment
        :param config_list: A list of objects that inherit Config
        :param output_path: The path where the experiment results will be dumped
        :param files_to_backup: A path or a list of paths (both directories or files work) to backup
        """
        self.experiment = experiment
        self.config_list = config_list
        self.log_list = []
        self.model_params_list = []
        self.output_path = output_path
        self.files_to_backup = files_to_backup

    def run(self):
        """
        Runs an experiment for each config in the config_list.
        """

        for config in self.config_list:
            # experiment related data is stored in self.experiment
            std_output_list, warnings_list, model_params = self._run_experiment(config)

            log = self._create_log_from_experiment_results(std_output_list, warnings_list)
            self.log_list.append(log)

            self.model_params_list.append(model_params)

    def save(self):
        utils.create_dir_if_it_does_not_exists(self.output_path)

        for i, (log, config, model_params) in enumerate(zip(self.log_list, self.config_list, self.model_params_list)):
            exp_results_dir_path = self.output_path + '/' + config.get_subdirectory_path
            utils.create_dir_if_it_does_not_exists(exp_results_dir_path)

            with open(exp_results_dir_path + '/config' + str(i) + '.out', 'wt') as out:
                pprint('Log:', stream=out)
                pprint(vars(log), stream=out)
                pprint('Config:', stream=out)
                pprint(vars(config), stream=out)

            utils.save_variables(exp_results_dir_path, model_params)
        self._copy_source_files(self.config_list[0].get_subdirectory_path)

    #TODO this function is ugly. Refactor.
    def _copy_source_files(self, destination_path):
        if self.files_to_backup is None:
            pass
        else:
            extended_destination_path = self.output_path + '/' + destination_path + '/backup'
            utils.create_dir_if_it_does_not_exists(extended_destination_path)

            if type(self.files_to_backup) is list:
                for i, file in enumerate(self.files_to_backup):
                    if os.path.isdir(file):
                        shutil.copytree(file, extended_destination_path + '/' + str(i),
                                        ignore=lambda x, y: self.output_path)
                    elif os.path.isfile(file):
                        file_name_without_directory = file.split('/')[-1]
                        shutil.copyfile(file, extended_destination_path + '/' + file_name_without_directory)

            elif type(self.files_to_backup) is str:
                if os.path.isdir(self.files_to_backup):
                    shutil.copytree(self.files_to_backup, extended_destination_path,
                                    ignore=lambda x, y: self.output_path)

                elif os.path.isfile(self.files_to_backup):
                    file_name_without_directory = self.files_to_backup.split('/')[-1]
                    shutil.copyfile(self.files_to_backup, extended_destination_path + '/' + file_name_without_directory)

            else:
                raise RuntimeWarning('files_to_backup must be a string or a list of strings')

    def _run_experiment(self, config):
        """
        Runs an experiment with a given config. Captures the warnings and std out writes.
        """
        with capturer.Capturing() as std_output_list:  # capture the stdout of an experiment
            with warnings.catch_warnings(record=True) as warnings_list:
                self.experiment.setup(config)
                self.experiment.run()
        return std_output_list, warnings_list, self.experiment.get_model_params()

    def _create_log_from_experiment_results(self, std_output_list, warnings_list):
        """
        Creates a Log object from the experiment outputs.
        """
        log = self.Log()
        log.exp_output = self.experiment.get_output()
        log.std_output = std_output_list
        log.method_runtimes = self.experiment.function_call_times
        log.warnings_list = warnings_list
        return log

    class Log:
        def __init__(self):
            self.uid = utils.get_uuid_hex_string()

        def __str__(self):
            return str(vars(self))
