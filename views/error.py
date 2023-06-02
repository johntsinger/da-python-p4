class ErrorView:
    R = "\033[0;31;40m"  # RED
    N = "\033[0m"  # Reset

    def date_error(self, value):
        message = f"\n'{value}' is not a date ! Please enter a date.\n"
        print()
        print(self.R+message+self.N)
        print()

    def digit_error(self, value):
        message = f"\n'{value}' is not a number ! Please enter a number.\n"
        print()
        print(self.R+message+self.N)
        print()

    def instance_exists(self, name):
        message = f"\nThis {name} already exists in the database.\n"
        print()
        print(self.R+message+self.N)
        print()

    def all_players_added(self):
        message = "All players are already registered for this tournament"
        print()
        print(self.R+message+self.N)
        print()

    def tournament_over(self):
        message = "All round of this tournement have already been set"
        print()
        print(self.R+message+self.N)
        print()

    def round_not_over(self):
        message = ("You can't start next round while the previous round"
                   " is not finished")
        print()
        print(self.R+message+self.N)
        print()

    def round_over(self):
        message = "This round is over !"
        print()
        print(self.R+message+self.N)
        print()

    def player_not_exist(self, response):
        message = f"Player with id {response} does not exist"
        print()
        print(self.R+message+self.N)
        print()

    def wrong_number_of_round(self, number_of_rounds, new_number_of_rounds):
        message = ("! Warning ! : The number of registered players does not" 
                   f" allow you to play {number_of_rounds} rounds"
                   f"\nThe number of rounds was set to {new_number_of_rounds}")
        print()
        print(self.R+message+self.N)
        print()

    def tournament_has_started(self):
        message = ("This tournament has alredy started,"
                   " so it's not possible to add more players !")
        print()
        print(self.R+message+self.N)
        print()
