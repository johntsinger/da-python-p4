import inspect


class CreateView:
    def info(self, name):
        message = (f"Informations to create a new {name}"
                   " (type <q> to abort creation)")
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
            print("Date format allowed :\n\n"
                  f"{' ' * 4}DDMMYY without separator\n"
                  f"{' ' * 4}or with separator DD-MM-YYYY or DD-MM-YY\n"
                  f"{' ' * 4}where separator can be spaces ' ', hyphens '-', "
                  " dots '.' or slash '/'")
            print()
        result = input(f"{label} : ")
        if not result:
            if not empty:
                print(f"\nA {name} must have a {label}\n")
            return None
        return result

    def accept(self, name, obj):
        print()
        print(obj)
        print()
        message = f"Save this {name} ? (y/n)"
        response = input(message)
        if response.lower() == "y" or not response:
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
        message = "Add players in this tournement"
        print()
        print(message)
        print()
