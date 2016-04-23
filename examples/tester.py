import experiment_runner
import examples.dummy_experiment as de
import examples.dummy_config as dc

config0 = dc.DummyConfig()
config1 = dc.DummyConfig()


experiment = de.DummyExperiment()
runner = experiment_runner.ExperimentRunner(experiment, [config0, config1])
runner.run()
runner.save_logs()

