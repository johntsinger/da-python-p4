class Frame:
    Y = "\033[0;33;40m"  # Yellow
    N = "\033[0m"  # Reset

    def frame(self, words):
        size = 100
        spaces = size - len(words)

        string = f"""
{"#" * (size + 4)}
# {" " * size} #
# {" " * int(spaces / 2)}{words}{" " * int(spaces / 2)} #
# {" " * size} #
{"#" * (size + 4)}\n
        """
        return self.Y+string+self.N


class TitleView(Frame):
    def main_title(self):
        print(self.frame("CHESS TOURNAMENT MANAGER"))

    def player_menu(self):
        print(self.frame("PLAYER MENU "))

    def new_player(self):
        print(self.frame("NEW PLAYER"))

    def delete_player(self):
        print(self.frame("DELETE PLAYER "))

    def players_list(self):
        print(self.frame("LIST OF PLAYERS "))

    def tournament_menu(self):
        print(self.frame("TOURNAMENT MENU "))

    def new_tournament(self):
        print(self.frame("NEW TOURNAMENT"))

    def delete_tournament(self):
        print(self.frame("DELETE TOURNAMENTS"))

    def search_tournament(self):
        print(self.frame("SEARCH TOURNAMENT "))

    def select_tournament(self):
        print(self.frame("SELECT TOURNAMENTS"))

    def rounds_list(self):
        print(self.frame("LIST OF ROUNDS"))

    def add_players(self):
        print(self.frame("ADD PLAYER FOR THIS TOURNAMENT"))

    def round_menu(self, round_number):
        print(self.frame(f"ROUND {round_number} "))
