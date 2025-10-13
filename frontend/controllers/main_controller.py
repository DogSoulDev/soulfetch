
from views.main_view import MainView

class MainController:
    def __init__(self):
        self.view = MainView()

    def run(self):
        self.view.show()
