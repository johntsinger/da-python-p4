import re
import dateutil.parser
from utils.tools import is_date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from views.manager import ViewsManager


class Validate:
    def __init__(self, views: 'ViewsManager'):
        self.views = views
        self.functions = {'date': self._validate_date,
                          'str': self._validate_str,
                          'int': self._validate_digit}

    @property
    def create_view(self):
        return self.views.create_view

    @property
    def error_view(self):
        return self.views.error_view

    @staticmethod  # need to be static to use it in the child class
    def _exists(instance_type: str):
        def inner(function):
            def wrapper(self, *args, **kwargs):
                new_instance = function(self, *args, **kwargs)
                for instance in self.instances:
                    if instance == new_instance:
                        self.error_view.instance_exists(instance_type)
                        new_instance = None
                        return new_instance
                return new_instance
            return wrapper
        return inner

    def _input(self, expected_type: str, label: str, empty: bool = False):
        result = None
        while not result:
            result = self.create_view.prompt_for(label, empty)
            result = self.functions[expected_type](result)
            if empty:  # can be empty for attributes with default value
                return result
        return result

    def _validate_date(self, result: str):
        if not is_date(result):
            self.error_view.date_error(result)
            return None
        return dateutil.parser.parse(result, dayfirst=True)

    def _validate_str(self, result: str):
        if not result:
            return None
        if re.match(r'\d', result):
            return None
        return result.strip().capitalize()

    def _validate_digit(self, result: str):
        if not result:
            return None
        if not result.isdigit():
            self.error_view.digit_error(result)
            return None
        return int(result)
