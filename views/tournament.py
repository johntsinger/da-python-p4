class TournamentMenuView:
    def display_tournaments(self, tournaments):
        for tournament in tournaments:
            print(f'\n[{tournament.uuid}] Tournament \n{tournament}')

    def select(self, name):
        message = f"Enter the number of the desired {name} : "
        response = input(message)
        try:
            int(response)
        except ValueError:
            return None
        return response

    def display_menu_interface(self):
        print("Create Tournament (0)    Select tournaments (1)    "
              "Delete tournament (6)    Return (9)")
        response = input()
        if response not in ['0', '1', '6', '9']:
            return None
        return response

    def display_interface(self):
        print("Add players (0)    Start (1)"
              "    Return (9)")
        response = input()
        if response not in ['0', '1', '9']:
            return None
        return response
