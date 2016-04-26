from sicco import experiment_runner, config, experiment
from sklearn import svm

class SVMConfig(config.Config):
    def __init__(self):
        super().__init__()
        self.description = {
            'code': 'svm_example',
            'description': 'A simple svm example'
        }
        self.X_train = [[0, 0], [1, 1]]
        self.y_train = [0, 1]
        self.X_test = [[2, 2]]
        self.y_test = [1]
        self.svm_C = 1.5

    def get_data(self):
        return (self.X_train, self.y_train, self.X_test, self.y_test)


class SVMExperiment(experiment.Experiment):
    @experiment.timeit
    def setup(self, config):
        self.X_train, self.y_train, self.X_test, self.y_test = config.get_data()
        self.clf = svm.SVC(C=config.svm_C)

    @experiment.timeit
    def run(self):
        self.clf.fit(self.X_train, self.y_train)
        self.score = self.clf.score(self.X_test, self.y_test)
        print('hi')
        # raise Warning('yo')

    def get_output(self):
        return {'accuracy': self.score}

    def get_model_params(self):
        return {'classifier': self.clf}


config0 = SVMConfig()
config1 = SVMConfig()

experiment = SVMExperiment()
runner = experiment_runner.ExperimentRunner(experiment, [config0, config1], files_to_backup='..')
runner.run()
runner.save()
