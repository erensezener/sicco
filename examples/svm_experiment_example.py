from sicco import experiment_runner, config, experiment
from sklearn import svm
import warnings


@experiment_runner.config
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
        return self.X_train, self.y_train, self.X_test, self.y_test


@experiment_runner.experiment(files_to_backup='..')
class SVMExperiment(experiment.Experiment):
    @experiment_runner.timeit
    def setup(self, config):
        self.X_train, self.y_train, self.X_test, self.y_test = config.get_data()
        self.clf = svm.SVC(C=config.svm_C)

    @experiment_runner.timeit
    def run(self):
        self.clf.fit(self.X_train, self.y_train)
        self.score = self.clf.score(self.X_test, self.y_test)
        warnings.warn('An example warning')

    def get_output(self):
        return {'accuracy': self.score}

    def get_model_params(self):
        return {'classifier': self.clf}
