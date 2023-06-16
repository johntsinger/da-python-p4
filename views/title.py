from utils.ansi_colors import Y, N


class Frame:
    def frame(self, words):
        """Create frame for tittle"""
        size = 100
        spaces = size - len(words)

        string = f"""
{"#" * (size + 4)}
# {" " * size} #
# {" " * int(spaces / 2)}{words}{" " * int(spaces / 2)} #
# {" " * size} #
{"#" * (size + 4)}\n
        """
        return Y+string+N


class TitleView(Frame):
    def main_title(self):
        print(self.frame("CHESS TOURNAMENT MANAGER"))

    def player_menu(self):
        print(self.frame("PLAYER MENU "))

    def new_player(self):
        print(self.frame("NEW PLAYER"))

    def delete_player(self):
        print(self.frame("DELETE PLAYER "))

    def export_players(self):
        print(self.frame("EXPORT PLAYERS"))

    def tournaments_menu(self):
        print(self.frame("TOURNAMENTS MENU"))

    def tournament_menu(self):
        print(self.frame("TOURNAMENT MENU "))

    def new_tournament(self):
        print(self.frame("NEW TOURNAMENT"))

    def delete_tournament(self):
        print(self.frame("DELETE TOURNAMENTS"))

    def search_tournament(self):
        print(self.frame("SEARCH TOURNAMENT "))

    def select_tournament(self):
        print(self.frame("SELECT TOURNAMENT "))

    def export_tournament(self):
        print(self.frame("EXPORT THIS TOURNAMENT"))

    def export_all_tournaments(self):
        print(self.frame("EXPORT ALL TOURNAMENT "))

    def rounds_list(self):
        print(self.frame("LIST OF ROUNDS"))

    def add_players(self):
        print(self.frame("ADD PLAYER FOR THIS TOURNAMENT"))

    def round_menu(self, round_number):
        print(self.frame(f"ROUND {round_number} "))
