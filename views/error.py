class ErrorView:
    R = "\033[0;31;40m"  # RED
    N = "\033[0m"  # Reset

    def display(self, message):
        print()
        print(self.R+message+self.N)
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

    def tournament_over(self):
        message = "All round of this tournement have already been set"
        self.display(message)

    def round_not_over(self):
        message = ("You can't start next round while the previous round"
                   " is not finished")
        self.display(message)

    def round_over(self):
        message = "This round is over !"
        self.display(message)

    def player_not_exist(self, response):
        message = f"Player with id {response} does not exist"
        self.display(message)

    def no_response(self):
        message = ("You must enter an id of a player to add him/her"
                   " to the tournament !\nYou can quit the selection"
                   " by pressing 'q'")
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
        message = (f"There is no {name} to display...\n"
                   "Please create at least one player")
        self.display(message)
