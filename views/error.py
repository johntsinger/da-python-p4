class ErrorView:
    def date_error(self, value):
        message = f"\n'{value}' is not a date ! Please enter a date.\n"
        print()
        print(message)
        print()

    def digit_error(self, value):
        message = f"\n'{value}' is not a number ! Please enter a number.\n"
        print()
        print(message)
        print()

    def instance_exists(self, name):
        message = f"\nThis {name} already exists in the database.\n"
        print()
        print(message)
        print()

    def all_players_added(self):
        message = "All players are already registered for this tournament"
        print()
        print(message)
        print()

    def tournament_ended(self):
        message = "All round of this tournement have already been set"
        print()
        print(message)
        print()

    def round_not_finished(self):
        message = "You can't start next round while the previous round is not finished"
        print()
        print(message)
        print()

    def player_not_exist(self, response):
        message = f"Player with id {response} does not exist"
        print()
        print(message)
        print()
