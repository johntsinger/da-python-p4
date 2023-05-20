class Frame:
    SEPARATOR = f"/n{'-'*40}/n"

    def sep(self):
        print(self.SEPARATOR)

    def frame(self, words):
        size = 50
        spaces = size - len(words)

        string = f"""
{"#" * (size + 4)}
# {" " * size} #
# {" " * int(spaces / 2)}{words}{" " * int(spaces / 2)} #
# {" " * size} #
{"#" * (size + 4)}\n
        """
        return string


class TitleView(Frame):
    def new_player_title(self):
        print(self.frame("NEW PLAYER"))

    def new_tournament_title(self):
        print(self.frame("NEW TOURNAMENT"))

    def main_title(self):
        print(self.frame("CHESS TOURNAMENT MANAGER"))

    def player_menu(self):
        print(self.frame("PLAYER MENU "))

    def tournament_menu(self):
        print(self.frame("TOURNAMENT MENU "))
