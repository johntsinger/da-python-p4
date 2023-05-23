class TournamentMenuView:
    def select(self, name):
        message = f"Enter the id of the desired {name}{' (type <q> to stop)' if name == 'player' else ''} : "
        response = input(message)
        try:
            int(response)
        except ValueError:
            if response.lower() == 'q':
                return response
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

    def display_player(self, player):
        print(f"\nPlayer : {player} has been added to the tournament\n")
