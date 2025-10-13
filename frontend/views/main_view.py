from PySide6.QtWidgets import QMainWindow, QLabel
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SoulFetch")
        self.setGeometry(100, 100, 800, 600)
        self.set_dark_theme()
        # Add central widget with text
        label = QLabel("Welcome to SoulFetch", self)
        label.setStyleSheet("color: #DCDCDE; font-size: 24px; background: transparent;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)
        self.setMinimumSize(400, 300)
        self.resize(800, 600)
        self.show()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(40, 40, 40))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(45, 45, 45))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.Button, QColor(50, 50, 50))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
        palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.ColorRole.Highlight, QColor(90, 90, 90))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor(220, 220, 220))
        self.setPalette(palette)
