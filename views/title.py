class Frame:
    SEPARATOR = f"/n{'-'*40}/n"

    def sep(self):
        print(self.SEPARATOR)

    def frame(self, *words):
        size = 50
        spaces = size - max(len(word) for word in words)
        print("#" * (size + 4))
        print(f"# {' ' * size} #")
        for word in words:
            print(f"# {' ' * int(spaces / 2)}{word}{' ' * int(spaces / 2)} #")
        print(f"# {' ' * size} #")
        print("#" * (size + 4))
        print()


class TitleView(Frame):
    def new_player_title(self):
        self.frame("NEW PLAYER")

    def new_tournament_title(self):
        self.frame("NEW TOURNAMENT")

    def main_title(self):
        self.frame("CHESS TOURNAMENT MANAGER")

    def player_menu(self):
        self.frame("PLAYER MENU ")

    def tournament_menu(self):
        self.frame("TOURNAMENT MENU ")
