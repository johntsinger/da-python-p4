import inspect


class CreateView:
    def info(self, name):
        message = (f"Informations to create a new {name}"
                   " (enter <q> to abort creation)")
        print(message)
        print()

    def prompt_for(self, label, empty):
        name = inspect.stack(
            )[1][0].f_locals['self'].__class__.__name__.replace('New', '')
        if label == 'Number of rounds':
            label += ' (can be left empty (default : 4 rounds))'
        elif label == 'Description of tournament':
            label += ' (can be left empty)'
        elif label in ('Start date', 'End date', 'Date of birth'):
            print()
            print("Date format allowed (hours and minutes can be omited):\n\n"
                  f"{' ' * 4}DDMMYY hhmm without separator\n"
                  f"{' ' * 4}or with separator DD/MM/YYYY hh:mm "
                  " or DD/MM/YY hh:mm\n"
                  f"{' ' * 4}Use DD/MM/YY hh if minutes not needed")
            print()
        result = input(f"{label} : ")
        if not result:
            if not empty:
                print(f"\nA {name} must have a {label}\n")
            return None
        return result

    def accept(self, name, obj):
        message = f"The {name} has been created :"
        print()
        print(message)
        print()
        print(obj)
        print()
        message = f"Save this {name} ? (y/n)"
        response = input(message)
        if response.lower() != "n" or not response:
            return True
        return False

    def load_data(self, name, data):
        message = f"Resume the latest {name} creation ? (y/n)"
        print()
        for key, value in data.items():
            if value:
                print(f"{key} : {value}")
        print()
        response = input(message)
        if response.lower() == "y" or not response:
            return True
        return False

    def add_player(self):
        message = ("Add players in this tournament\n\n"
                   "You don't need to add players right away"
                   " - that can be done later.")
        print()
        print(message)
        print()
