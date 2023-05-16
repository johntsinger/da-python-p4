import os
import dateutil.parser


def is_date(string):
    try:
        dateutil.parser.parse(string)
        return True
    except ValueError:
        return False
    except TypeError:
        return False


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')
