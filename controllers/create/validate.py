import re
import dateutil.parser
from models.exceptions import UserExitException
from utils.tools import is_date


class Validate:
    """Validation class"""
    def __init__(self, views):
        self.views = views
        self.functions = {'date': self._validate_date,
                          'str': self._validate_str,
                          'int': self._validate_digit}

    @property
    def create_view(self):
        return self.views.create

    @property
    def error_view(self):
        return self.views.error

    @staticmethod  # need to be static to use it in the child class
    def _exists(instance_type):
        """Function that return a decorator to check if instance of
        new player or new tournament already exists.

        params :
            - instance_type (str) :
                the type on the instance (i.e. 'tounrament').
                Used to display error message
        """
        def inner(function):
            def wrapper(self, *args, **kwargs):
                new_instance = function(self, *args, **kwargs)
                for instance in self.instances:
                    if instance == new_instance:
                        self.error_view.instance_exists(instance_type)
                        new_instance = None
                return new_instance
            return wrapper
        return inner

    def _input(self, expected_type, label, empty=False):
        """Validate user inputs.
            params:
                - expected_type (str) : the type expected
                - label (str) : the label that will be asked from the user
                - empty (bool default=False) : to allow the user's reponse
                                               to be empty
        """
        result = None
        while not result:
            result = self.create_view.prompt_for(label, empty)
            if result == 'q':
                raise UserExitException
            result = self.functions[expected_type](result)
            if empty:  # can be empty for attributes with default value
                return result
        return result

    def _validate_date(self, result):
        if not result:
            return None
        elif not is_date(result):
            self.error_view.date_error(result)
            return None
        return dateutil.parser.parse(result, dayfirst=True)

    def _validate_str(self, result):
        if not result:
            return None
        if re.match(r'\d', result):
            self.error_view.str_error(result)
            return None
        return result.strip().capitalize()

    def _validate_digit(self, result):
        if not result:
            return None
        elif not result.isdigit():
            self.error_view.digit_error(result)
            return None
        return int(result)
