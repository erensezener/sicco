import experiment
import time


class DummyExperiment(experiment.Experiment):
    def __init__(self):
        super().__init__()
        self.echo_string = ""

    @experiment.timeit
    def setup(self, config):
        self.echo_string = config.echo_string

    @experiment.timeit
    def run(self):
        time.sleep(1)
        print(self.echo_string)

    def get_output(self):
        return self.echo_string
