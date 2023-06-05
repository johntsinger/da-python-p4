class TournamentMenuView:
    def select(self, name):
        message = (f"Enter the id of the desired {name}"
                   f"{' (type <q> to stop)' if name == 'player' else ''} : ")
        response = input(message)
        try:
            int(response)
        except ValueError:
            if response.lower() == 'q':
                return response.lower()
            return None
        return response

    def display_player(self, player):
        print(f"\nPlayer : {player} has been added to the tournament\n")

    def prompt_for(self, label):
        result = input(f"{label} : ")
        return result

    def search_info(self):
        message = "Search a tournament by it's name and it's start date"
        print(message)
        print()
