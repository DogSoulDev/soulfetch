

from PySide6.QtWidgets import QApplication
from frontend.controllers.main_window_controller import MainWindowController
import sys

if __name__ == "__main__":
    print("[SoulFetch] Iniciando aplicación...")
    app = QApplication(sys.argv)
    controller = MainWindowController()
    print("[SoulFetch] Mostrando ventana principal...")
    controller.run()
    print("[SoulFetch] Ventana principal mostrada. Esperando eventos...")
    sys.exit(app.exec())
