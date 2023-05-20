import inspect


class CreateView:
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
        print(obj)
        message = f"Save this {name} ? (y/n)"
        response = input(message)
        if response == "y" or not response:
            return True
        return False
