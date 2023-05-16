from controllers.home import Home


class Controller:
    def __init__(self, views):
        self.views = views
        self.home = Home(views)

    def run(self):
        running = True
        while running:
            self.home.manager()
