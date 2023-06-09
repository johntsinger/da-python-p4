class InterfaceView:
    OPTIONS = {
        "home": {
            "label": (
                f"Player menu (1){' ' * 4}"
                f"Tournaments menu (2){' ' * 4}"
                "Exit (9)"
            ),
            "key": [
                "1", "2", "9"
            ]
        },
        "player": {
            "label": (
                f"Create player (1){' ' * 4}"
                f"Export all players (2){' ' * 4}"
                f"Delete player (6){' ' * 4}"
                "Return (9)"
            ),
            "key": [
                "1", "2", "6", "9"
            ]
        },
        "tournament": {
            "label": (
                f"Create tournament (1){' ' * 4}"
                f"Select tournament (2){' ' * 4}"
                f"Search tournament (3){' ' * 4}"
                f"Export all tournaments (4){' ' * 4}"
                f"Delete tournament (6){' ' * 4}"
                "Return (9)"
            ),
            "key": [
                "1", "2", "3", "4", "6", "9"
            ]
        },
        "tournament_menu": {
            "label": (
                f"Add players (1){' ' * 4}"
                f"Start (2){' ' * 4}"
                f"Export player (3){' ' * 4}"
                f"Export rounds (4){' ' * 4}"
                f"Export tournament (5){' ' * 4}"
                f"Withdraw player (6){' ' * 4}"
                "Return (9)"
            ),
            "key": [
                "1", "2", "3", "4", "5", "6", "9"
            ]
        },
        "round": {
            "label": (
                f"Select winner (1){' ' * 4}"
                f"Next round (2){' ' * 4}"
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
