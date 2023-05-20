class RoundView:
    def select(self, name):
        message = f"Enter the number of the desired {name} : "
        response = input(message)
        try:
            int(response)
        except ValueError:
            return None
        return response

    def prompt_for_winner(self, match):
        message = f"Select the winner for match : {match}"
        print(message)

    def prompt_for_next_round(self):
        message = "Next round ? (y/n) : "
        response = input(message)
        if response == 'y' or not response:
            return True
        return False