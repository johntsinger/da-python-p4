class PlayerMenuView:
    def display_interface(self):
        print("Create Player (0)    Display all players (1)    "
              "Delete Player (6)   Return (9)")
        response = input()
        if response not in ['0', '1', '6', '9']:
            return None
        return response

    def select(self, name):
        message = f"Enter the id of the desired {name} : "
        response = input(message)
        try:
            int(response)
        except ValueError:
            return None
        return response
