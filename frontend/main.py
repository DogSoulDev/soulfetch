
from PySide6.QtWidgets import QApplication
from controllers.main_controller import MainController
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    controller = MainController()
    controller.run()
    sys.exit(app.exec())
