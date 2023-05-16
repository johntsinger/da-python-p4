class ErrorView:
    def date_error(self, value):
        message = f"\n'{value}' is not a date ! Please enter a date.\n"
        print(message)

    def digit_error(self, value):
        message = f"\n'{value}' is not a number ! Please enter a number.\n"
        print(message)

    def instance_exists(self, name):
        message = f"\nThis {name} already exists in the database.\n"
        print(message)

    def all_players_added(self):
        message = "All players are already registered for this tournament"
        print(message)