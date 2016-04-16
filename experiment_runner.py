import capturer


class ExperimentRunner:
    def __init__(self, experiment, config_list):
        self.experiment = experiment
        self.config_list = config_list
        self.logs = []

    def run(self):
        for config in self.config_list:
            with capturer.Capturing() as std_output:  # capture the stdout of an experiment
                log = self.Log()

                self.experiment.setup(config)
                self.experiment.run()

                log.exp_output = self.experiment.get_output()
                log.std_output = std_output
                log.run_time = self.experiment.function_call_times

                self.logs.append(log)

    def dump(self):
        print('dumping')
        for log in self.logs:
            print('Exp output: {}' .format(log.exp_output))
            print('Std output: {}' .format(log.std_output))
            print('Times: {}' .format(log.run_time))



    class Log:
        pass
