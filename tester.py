import experiment_runner
import dummy_experiment as de

config0 = lambda : None #create a class inline
config0.echo_string = 'a'

config1 = lambda : None
config1.echo_string = 'b'

experiment = de.DummyExperiment()
runner = experiment_runner.ExperimentRunner(experiment, [config0, config1])
runner.run()
runner.dump()



