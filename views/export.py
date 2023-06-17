class ExportToHTML:
    def export(self):
        message = "Do you want to export this report ? (y/n)"
        response = input(message)
        if response.lower() == "y":
            return True
        return False

    def export_confirmation(self, name):
        message = ("This report has been exported !"
                   f" You can find it in ../html-report/{name}.html")
        print()
        print(message)
        print()
