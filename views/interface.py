class InterfaceView:
    OPTIONS = {
        "home": {
            "label": (
                f"Player menu (1){' ' * 4}"
                f"Tournament menu (2){' ' * 4}"
                "Exit (9)"
            ),
            "key": [
                "1", "2", "9"
            ]
        },
        "player": {
            "label": (
                f"Create Player (1){' ' * 4}"
                f"Display all players (2){' ' * 4}"
                f"Delete Player (6){' ' * 4}"
                "Return (9)"
            ),
            "key": [
                "1", "2", "6", "9"
            ]
        },
        "tournament": {
            "label": (
                f"Create Tournament (1){' ' * 4}"
                f"Select tournaments (2){' ' * 4}"
                f"Delete tournament (6){' ' * 4}"
                "Return (9)"
            ),
            "key": [
                "1", "2", "6", "9"
            ]
        },
        "tournament_menu": {
            "label": (
                f"Add players (1){' ' * 4}"
                f"Start (2){' ' * 4}"
                "Return (9)"
            ),
            "key": [
                "1", "2", "9"
            ]
        }
    }

    def display_interface(self, name):
        print(self.OPTIONS[name]['label'])
        response = input()
        if response not in self.OPTIONS[name]['key']:
            return None
        return response