from utils.ansi_colors import R, G, N


class TournamentMenuView:
    def select(self, name, to_stop=False):
        if to_stop:
            to_stop_message = '(enter <q> to stop)'
        else:
            to_stop_message = '(press `return` to return)'
        message = f"Enter the id of the desired {name} {to_stop_message} : "
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
        if label == 'Start date':
            print()
            print("Date format allowed (hours and minutes can be omited):\n\n"
                  f"{' ' * 4}DDMMYY hhmm without separator\n"
                  f"{' ' * 4}or with separator DD/MM/YYYY hh:mm "
                  " or DD/MM/YY hh:mm\n"
                  f"{' ' * 4}Use DD/MM/YY hh if minutes not needed")
            print()
        result = input(f"{label} : ")
        return result

    def search_info(self):
        message = "Search a tournament by it's name and it's start date"
        print(message)
        print()

    def tie_breaking_info(self):
        message = "Tie-breaking system : Buchholz (Bu.) and Cumulative (Cu.)"
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
        else:
            return False

    def players_sort_info(self):
        message = "This rapport is sorted in alphabetical order"
        print()
        print(message)
        print()

    def short_form_info(self):
        message = "Nuber of rounds (NR), Curent round (CR)"
        print(message)
        print()
