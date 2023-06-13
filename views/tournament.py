from utils.ansi_colors import R, G, N


class TournamentMenuView:
    def select(self, name):
        message = (f"Enter the id of the desired {name}"
                   f"{' (enter <q> to stop)' if name == 'player' else ''} : ")
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

    def accept_delete(self, name, item):
        indent = ' ' * 4 if name == 'player' else ''
        message = (f"Delete the {name} :\n\n{indent}{item}\n\n"
                   "Are you sure ? (y/n) :")
        # remove existing ansi code
        message = message.replace(G, '').replace(N, '')
        print()
        response = input(R+message+N)
        print()
        if response.lower() == "y":
            return True
        return False
