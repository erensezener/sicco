import sicco_config
import utils
import config


class DummyConfig(config.Config):
    def __init__(self):
        super().__init__()
        self.echo_string = 'lolo'