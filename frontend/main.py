

from PySide6.QtWidgets import QApplication
from .controllers.main_window_controller import MainWindowController
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MainWindowController()
    controller.run()
    sys.exit(app.exec())
