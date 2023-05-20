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
        print(f"Select the winner for match : {match}")