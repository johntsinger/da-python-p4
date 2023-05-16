from views.manager import ViewsManager
from controllers.base import Controller


def main():
    views = ViewsManager()
    controller = Controller(views)
    controller.run()


if __name__ == '__main__':
    main()