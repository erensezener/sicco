import warnings
import capturer
import utils
from pprint import pprint


class ExperimentRunner(object):
    def __init__(self, experiment, config_list, output_path='./sicco_logs'):
        self.experiment = experiment
        self.config_list = config_list
        self.log_list = []
        self.model_params_list = []
        self.output_path = output_path

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

    def save_logs(self):
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

    class Log:
        def __init__(self):
            self.uid = utils.get_uuid_hex_string()

        def __str__(self):
            return str(vars(self))
