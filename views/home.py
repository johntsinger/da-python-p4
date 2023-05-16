class HomeView():
    def display_interface(self):
        print("Player menu (0)    Tournament menu (1)    Exit (9)")
        response = input()
        if response not in ['0', '1', '9']:
            return None
        return response
