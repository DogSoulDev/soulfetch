from ..views.main_window import MainWindow

class MainWindowController:
    def __init__(self):
        self.view = MainWindow()

    def run(self):
        self.view.show()

    def notify(self, message, success=True, duration=3000):
        """
        Show a floating notification (toast) in the main window.
        """
        self.view.show_toast(message, success=success, duration=duration)
