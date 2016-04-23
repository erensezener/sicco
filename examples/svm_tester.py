import experiment_runner
import examples.svm_experiment as se
import examples.svm_config as sc

config0 = sc.SVMConfig()
config1 = sc.SVMConfig()


experiment = se.SVMExperiment()
runner = experiment_runner.ExperimentRunner(experiment, [config0, config1])
runner.run()
runner.save_logs()

