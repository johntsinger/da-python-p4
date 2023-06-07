class RoundView:
    def select(self, name, players=None):
        print()
        if name == "winner":
            message = (f"(1) {players[0]}    (2) {players[1]}    (3) draw"
                       "\n\nSelect the winner : ")
        else:
            message = (f"Enter the id of the desired {name}"
                       " (press `return` to return) : ")
        response = input(message)
        print()
        try:
            int(response)
        except ValueError:
            if response.lower() == 'q':
                return response.lower()
            else:
                return None
        return response

    def prompt_for_winner(self, match):
        message = f"Select the winner for match : {match}"
        print(message)
        print()

    def prompt_for_next_round(self):
        print()
        message = "Next round ? (y/n) : "
        response = input(message)
        if response.lower() == 'y' or not response:
            return True
        return False
