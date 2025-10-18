
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PySide6.QtWidgets import QApplication
from controllers.main_window_controller import MainWindowController
import sys

if __name__ == "__main__":
    import subprocess
    import time
    print("[SoulFetch] Starting backend API server...")
    backend_proc = subprocess.Popen([sys.executable, '-m', 'backend.main'])
    time.sleep(2)  # Give backend time to start
    print("[SoulFetch] Backend API server started.")
    app = QApplication(sys.argv)
    controller = MainWindowController()
    print("[SoulFetch] Showing main window...")
    controller.run()
    print("[SoulFetch] Main window shown. Waiting for events...")
    exit_code = app.exec()
    print("[SoulFetch] Shutting down backend API server...")
    backend_proc.terminate()
    backend_proc.wait()
    print("[SoulFetch] Backend API server stopped.")
    sys.exit(exit_code)
