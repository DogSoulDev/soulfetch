from ..views.main_window import MainWindow

class MainWindowController:
    def __init__(self):
        self.view = MainWindow()

    def run(self):
        self.view.show()
