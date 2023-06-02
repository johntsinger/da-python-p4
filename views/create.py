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
