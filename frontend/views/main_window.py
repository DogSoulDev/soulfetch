from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QHBoxLayout, QStatusBar,
    QVBoxLayout, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPalette, QColor, QIcon
from .request_tab import RequestTab
from .history_tab import HistoryTab
from .test_runner_tab import TestRunnerTab
from .mock_tab import MockTab
from .environment_manager_tab import EnvironmentManagerTab
from .auth_tab import AuthTab
from .response_visualizer_tab import ResponseVisualizerTab
from .request_scheduler_tab import RequestSchedulerTab
from .plugin_manager_tab import PluginManagerTab
from .user_manager_tab import UserManagerTab
from .cloud_sync_tab import CloudSyncTab
from .codegen_tab import CodeGenTab
from .accessibility_tab import AccessibilityTab
from .visualization_tab import VisualizationTab
from .workspace_tab import WorkspaceTab

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("SoulFetch API Client")
        self.setGeometry(100, 100, 1100, 700)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready | No environment selected | No errors")

        # Modern dark theme
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(40, 44, 52))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(30, 34, 40))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(44, 48, 56))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(50, 54, 62))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(80, 120, 200))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        self.setPalette(dark_palette)

        # Main tab widget (fully centralized, no sidebar)
        import requests
        self.tabs = QTabWidget()
        self.tabs.addTab(RequestTab(), "Request Builder")
        self.tabs.addTab(HistoryTab(), "History")
        self.tabs.addTab(TestRunnerTab(), "Test Runner")
        # Mock Server
        try:
            r = requests.get("http://127.0.0.1:8000/mock_server", timeout=2)
            if r.status_code == 200:
                self.tabs.addTab(MockTab(), "Mock Server")
        except Exception:
            pass
        # Cloud Sync
        try:
            r = requests.get("http://127.0.0.1:8000/cloud/sync", timeout=2)
            if r.status_code == 200:
                self.tabs.addTab(CloudSyncTab(), "Cloud Sync")
        except Exception:
            pass
        # CodeGen
        try:
            r = requests.get("http://127.0.0.1:8000/codegen", timeout=2)
            if r.status_code == 200:
                self.tabs.addTab(CodeGenTab(), "CodeGen")
        except Exception:
            pass
        # Visualization
        try:
            r = requests.get("http://127.0.0.1:8000/visualization/data", timeout=2)
            if r.status_code == 200:
                self.tabs.addTab(VisualizationTab(), "Visualization")
        except Exception:
            pass
        # Workspace Collaboration
        try:
            r = requests.get("http://127.0.0.1:8000/workspace/demo", timeout=2)
            if r.status_code == 200:
                self.tabs.addTab(WorkspaceTab(), "Workspace Collaboration")
        except Exception:
            pass
        self.tabs.addTab(EnvironmentManagerTab(), "Environments")
        self.tabs.addTab(RequestSchedulerTab(), "Scheduler/Monitor")
        self.tabs.addTab(PluginManagerTab(), "Plugins/Scripting")
        self.tabs.addTab(UserManagerTab(), "User Management")
        self.tabs.addTab(AccessibilityTab(), "Accessibility/i18n")
        self.tabs.setCurrentIndex(0)

        # Botón + New Request sobre las pestañas
        tabbar_layout = QVBoxLayout()
        tabbar_layout.setContentsMargins(0, 0, 0, 0)
        tabbar_layout.setSpacing(0)
        self.new_request_btn = QPushButton("+ New Request")
        self.new_request_btn.setStyleSheet("font-weight: bold; background: #222; color: #8be9fd; border-radius: 6px; padding: 6px 18px;")
        self.new_request_btn.clicked.connect(self.add_request_tab)
        tabbar_layout.addWidget(self.new_request_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        tabbar_layout.addWidget(self.tabs)
        tabbar_container = QWidget()
        tabbar_container.setLayout(tabbar_layout)
        tabbar_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Layout principal: solo el área de pestañas
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(tabbar_container)
        central_widget.setLayout(central_layout)
        central_widget.setMinimumSize(600, 400)
        self.setCentralWidget(central_widget)

    def add_request_tab(self):
        tab = RequestTab()
        self.tabs.addTab(tab, "Request Builder")
        self.tabs.setCurrentWidget(tab)

        # Botón + New Request sobre las pestañas
        tabbar_layout = QVBoxLayout()
        tabbar_layout.setContentsMargins(0, 0, 0, 0)
        tabbar_layout.setSpacing(0)
        self.new_request_btn = QPushButton("+ New Request")
        self.new_request_btn.setStyleSheet("font-weight: bold; background: #222; color: #8be9fd; border-radius: 6px; padding: 6px 18px;")
        self.new_request_btn.clicked.connect(self.add_request_tab)
        tabbar_layout.addWidget(self.new_request_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        tabbar_layout.addWidget(self.tabs)
        tabbar_container = QWidget()
        tabbar_container.setLayout(tabbar_layout)
        tabbar_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Layout principal: solo el área de pestañas
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(tabbar_container)
        central_widget.setLayout(central_layout)
        central_widget.setMinimumSize(600, 400)
        self.setCentralWidget(central_widget)

        # Modern QSS
        self.setStyleSheet('''
            QMainWindow, QWidget {
                background-color: #282c34;
                color: #e0e0e0;
                font-size: 13px;
            }
            QTabWidget::pane { border: 1px solid #23252b; top: -1px; background: #23252b; }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #23252b, stop:1 #282c34);
                color: #8be9fd;
                border: 1px solid #23252b;
                border-bottom: none;
                padding: 6px 16px;
                min-width: 90px;
                font-weight: bold;
                border-radius: 8px 8px 0 0;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #44475a, stop:1 #282c34);
                color: #f8f8f2;
                border-bottom: 2px solid #ff79c6;
            }
            QTabBar::tab:hover {
                background: #343746;
            }
            QStatusBar {
                background: #23252b;
                color: #8be9fd;
                border-top: 1px solid #44475a;
                font-size: 13px;
            }
            QPushButton, QToolButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #393e4a, stop:1 #23252b);
                color: #e0e0e0;
                border: 1.5px solid #44475a;
                border-radius: 7px;
                padding: 5px 12px;
                font-size: 13px;
                font-weight: 500;
            }
        ''')

        # Context menu for tabs
        self.tabs.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.show_tab_context_menu)

    def show_tab_context_menu(self, pos):
        from PySide6.QtWidgets import QMenu, QInputDialog, QFileDialog, QMessageBox
        from PySide6.QtGui import QAction
        tab_index = self.tabs.tabBar().tabAt(pos)
        if tab_index < 0:
            return
        menu = QMenu(self)
        action_duplicate = QAction("Duplicate Tab", self)
        action_duplicate.triggered.connect(lambda: self.duplicate_tab(tab_index))
        menu.addAction(action_duplicate)
        action_close = QAction("Close Tab", self)
        action_close.triggered.connect(lambda: self.tabs.removeTab(tab_index))
        menu.addAction(action_close)
        action_close_others = QAction("Close Other Tabs", self)
        action_close_others.triggered.connect(lambda: self.close_other_tabs(tab_index))
        menu.addAction(action_close_others)
        action_rename = QAction("Rename Tab", self)
        action_rename.triggered.connect(lambda: self.rename_tab(tab_index))
        menu.addAction(action_rename)
        action_export = QAction("Export Tab", self)
        action_export.triggered.connect(lambda: self.export_tab(tab_index))
        menu.addAction(action_export)
        menu.exec_(self.tabs.tabBar().mapToGlobal(pos))

    def duplicate_tab(self, tab_index):
        # Duplicate the tab (deep copy if possible)
        tab_widget = self.tabs.widget(tab_index)
        tab_name = self.tabs.tabText(tab_index)
        import copy
        try:
            new_tab = copy.deepcopy(tab_widget)
        except Exception:
            # Fallback: create new instance if deepcopy fails
            new_tab = type(tab_widget)()
        self.tabs.addTab(new_tab, tab_name + " (Copy)")
        self.tabs.setCurrentWidget(new_tab)

    def close_other_tabs(self, tab_index):
        # Close all tabs except the selected one
        for i in reversed(range(self.tabs.count())):
            if i != tab_index:
                self.tabs.removeTab(i)

    def rename_tab(self, tab_index):
        from PySide6.QtWidgets import QInputDialog
        old_name = self.tabs.tabText(tab_index)
        new_name, ok = QInputDialog.getText(self, "Rename Tab", "New name:", text=old_name)
        if ok and new_name and new_name != old_name:
            self.tabs.setTabText(tab_index, new_name)

    def export_tab(self, tab_index):
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import os
        tab_name = self.tabs.tabText(tab_index)
        fname, _ = QFileDialog.getSaveFileName(self, "Export Tab", f"{tab_name}.txt", "Text Files (*.txt)")
        if fname:
            # Security: prevent path traversal
            if os.path.isabs(fname) and not fname.startswith(os.getcwd()):
                QMessageBox.critical(self, "Export Error", "[SECURITY] Invalid file path.")
                return
            try:
                # Try to export tab content as text (customize per tab type)
                tab_widget = self.tabs.widget(tab_index)
                content = str(tab_widget)
                with open(fname, 'w', encoding='utf-8') as f:
                    f.write(content)
                QMessageBox.information(self, "Export", f"Tab '{tab_name}' exported to {fname}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", str(e))