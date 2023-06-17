from utils.ansi_colors import R, N


class PlayerMenuView:
    def select(self, name):
        message = (f"Enter the id of the desired {name}"
                   " (press `return` to return) : ")
        response = input(message)
        try:
            int(response)
        except ValueError:
            return None
        return response

    def accept_delete(self, player):
        message = (f"Delete the player :\n\n{' ' * 4}{player}\n\n"
                   "Are you sure? (y/n) :")
        print()
        response = input(R+message+N)
        print()
        if response.lower() == "y":
            return True
        return False

    def players_sort_info(self):
        message = "This rapport is sorted in alphabetical order"
        print()
        print(message)
        print()
