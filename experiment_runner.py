import warnings

import capturer


class ExperimentRunner(object):
    def __init__(self, experiment, config_list):
        self.experiment = experiment
        self.config_list = config_list
        self.logs = []

    def run(self):
        for config in self.config_list:
            # experiment related data is stored in self.experiment
            std_output_list, warnings_list = self._run_experiments(config)

            log = self._log_experiment_results(std_output_list, warnings_list)
            self.logs.append(log)

    def _run_experiments(self, config):
        with capturer.Capturing() as std_output_list:  # capture the stdout of an experiment
            with warnings.catch_warnings(record=True) as warnings_list:
                self.experiment.setup(config)
                self.experiment.run()
        return std_output_list, warnings_list

    def _log_experiment_results(self, std_output_list, warnings_list):
        log = self.Log()
        log.exp_output = self.experiment.get_output()
        log.std_output = std_output_list
        log.method_runtimes = self.experiment.function_call_times
        return log

    def dump(self):
        print('dumping')
        for log in self.logs:
            print('Exp output: {}'.format(log.exp_output))
            print('Std output: {}'.format(log.std_output))
            print('Times: {}'.format(log.method_runtimes))

    class Log:
        def __init__(self):
            self.exp_output = None
            self.std_output = None
            self.method_runtimes = None
            self.warnings_list = None

        def dump(self):


