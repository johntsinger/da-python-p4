class PlayerMenuView:
    def select(self, name):
        message = f"Enter the id of the desired {name} : "
        response = input(message)
        try:
            int(response)
        except ValueError:
            return None
        return response
