from sicco import utils


class Config(object):
    """
    Please do not edit this class.
    Just override the constructor from the subclass and set the parameters in __init__().
    """
    def __init__(self):
        self.description = {
            'code': 'untitled_config',
            'description': 'no description is given'
        }

        self._experiment_date = utils.get_time_date_string()
        # self.uid = utils.get_uuid_hex_string()

    @property
    def get_subdirectory_path(self):
        return self.description['code'] + '/' + self._experiment_date

    def __str__(self):
        return str(vars(self))
