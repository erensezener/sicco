import config


class SVMConfig(config.Config):
    def __init__(self):
        super().__init__()
        self.X_train = [[0, 0], [1, 1]]
        self.y_train = [0, 1]
        self.X_test = [[2, 2]]
        self.y_test = [1]
        self.svm_C = 1.5

    def get_data(self):
        return (self.X_train, self.y_train, self.X_test, self.y_test)
