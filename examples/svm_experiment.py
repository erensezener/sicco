import experiment
from sklearn import svm


class SVMExperiment(experiment.Experiment):
    @experiment.timeit
    def setup(self, config):
        self.X_train, self.y_train, self.X_test, self.y_test = config.get_data()
        self.clf = svm.SVC(C=config.svm_C)

    @experiment.timeit
    def run(self):
        self.clf.fit(self.X_train, self.y_train)
        self.score = self.clf.score(self.X_test, self.y_test)

    def get_output(self):
        return {'accuracy': self.score}

    def get_model_params(self):
        return {'classifier': self.clf}
