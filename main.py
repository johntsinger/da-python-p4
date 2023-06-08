from views.manager import ViewsManager
from controllers.home import Home


def main():
    views = ViewsManager()
    controller = Home(views)
    controller.manager()


if __name__ == '__main__':
    main()
