from utils.ansi_colors import R, N


class ErrorView:
    def display(self, message):
        print()
        print(R+message+N)
        print()

    def date_error(self, value):
        message = f"'{value}' is not a date ! Please enter a date."
        self.display(message)

    def digit_error(self, value):
        message = f"'{value}' is not a number ! Please enter a number."
        self.display(message)

    def str_error(self, value):
        message = f"'{value}' is not a valid ! Please enter a string."
        self.display(message)

    def instance_exists(self, name):
        message = f"This {name} already exists in the database."
        self.display(message)

    def all_players_added(self):
        message = "All players are already registered for this tournament"
        self.display(message)

    def round_tournament_over(self):
        message = "All rounds of this tournement have already been set"
        self.display(message)

    def tournament_over(self):
        message = "This tournament is over ! You can't delete player anymore"
        self.display(message)

    def round_not_over(self):
        message = ("You can't start next round while the previous round"
                   " is not over")
        self.display(message)

    def round_over(self):
        message = "This round is over !"
        self.display(message)

    def player_required(self):
        message = ("You cannot start a tournament with fewer than 2 players\n"
                   "Please add players first to start this tournament")
        self.display(message)

    def not_exist(self, name, response):
        if response:
            message = f"{name.capitalize()} with id {response} does not exist"
        else:
            message = "The id must be an integer"
        self.display(message)

    def wrong_number_of_round(self, number_of_rounds, new_number_of_rounds):
        message = ("! Warning ! : The number of registered players does not"
                   f" allow you to play {number_of_rounds} rounds"
                   f"\nThe number of rounds was set to {new_number_of_rounds}")
        self.display(message)

    def tournament_has_started(self):
        message = ("This tournament has alredy started,"
                   " so it's not possible to add more players !")
        self.display(message)

    def nothing_to_display(self, name):
        message = (f"There are no {name}s... "
                   f"Please create at least one {name}")
        self.display(message)

    def not_enough_player(self):
        message = ("There are not enough players left to continue"
                   " this tournament")
        self.display(message)

    def no_tournament_found(self, name, date):
        message = ("No tournaments found with the name :"
                   f" {name} and stating on : {date}")
        self.display(message)
