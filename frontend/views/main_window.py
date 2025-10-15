from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QStatusBar, QMenu, QFileDialog, QTextEdit, QSizePolicy
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWebEngineWidgets import QWebEngineView
from .collection_sidebar import CollectionSidebar
from .environment_modal import EnvironmentModal
# ToastNotification widget for floating messages
class ToastNotification(QLabel):
    def __init__(self, message, parent=None, duration=3000, success=True):
        super().__init__(parent)
        self.setText(message)
        self.setStyleSheet(f"""
            background-color: {'#2ecc40' if success else '#e74c3c'};
            color: white;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        """)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.ToolTip)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        QTimer.singleShot(duration, self.close)

    def show_at_bottom_right(self, main_window):
        geo = main_window.geometry()
        self.adjustSize()
        x = geo.x() + geo.width() - self.width() - 40
        y = geo.y() + geo.height() - self.height() - 40
        self.move(x, y)
        self.show()

class MainWindow(QMainWindow):
    def send_to_response_visualizer(self, response_text):
        self.response_visualizer_tab.data_edit.setText(response_text)
        self.tabs.setCurrentWidget(self.response_visualizer_tab)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SoulFetch API Client")
        self.setGeometry(100, 100, 1200, 800)
        self.set_dark_theme()

        # Global Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready | No environment selected | No errors")

        # Sidebar: Collections & History
        self.sidebar_widget = CollectionSidebar()
        self.sidebar_widget.collection_selected.connect(self.load_collection_request)
        self.env_modal = EnvironmentModal(self)
        env_btn = QPushButton("Manage Environments")
        env_btn.clicked.connect(self.open_env_modal)
        self.sidebar_widget.sidebar_layout.addWidget(env_btn)

        # Tabs: Request Builder
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.show_tab_context_menu)
        self.add_request_tab()
        self.add_history_tab()
        self.add_gemini_tab()
        from .test_runner_tab import TestRunnerTab
        self.test_runner_tab = TestRunnerTab()
        self.tabs.addTab(self.test_runner_tab, "Test Runner")
        from .mock_tab import MockTab
        self.mock_tab = MockTab()
        self.tabs.addTab(self.mock_tab, "Mock Server")
        from .flow_designer_tab import FlowDesignerTab
        self.flow_designer_tab = FlowDesignerTab()
        self.tabs.addTab(self.flow_designer_tab, "Flow Designer")
        from .environment_manager_tab import EnvironmentManagerTab
        self.environment_manager_tab = EnvironmentManagerTab()
        self.tabs.addTab(self.environment_manager_tab, "Environments")
        from .auth_tab import AuthTab
        self.auth_tab = AuthTab()
        self.tabs.addTab(self.auth_tab, "Auth")
        from .response_visualizer_tab import ResponseVisualizerTab
        self.response_visualizer_tab = ResponseVisualizerTab()
        self.tabs.addTab(self.response_visualizer_tab, "Response Visualizer")
        from .request_scheduler_tab import RequestSchedulerTab
        self.request_scheduler_tab = RequestSchedulerTab()
        self.tabs.addTab(self.request_scheduler_tab, "Scheduler/Monitor")
        from .plugin_manager_tab import PluginManagerTab
        self.plugin_manager_tab = PluginManagerTab()
        self.tabs.addTab(self.plugin_manager_tab, "Plugins/Scripting")

        # Layout: sidebar | tabs
        main_layout = QHBoxLayout()
        self.sidebar_widget.setMinimumWidth(220)
        self.sidebar_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.tabs.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.sidebar_widget, 1)
        main_layout.addWidget(self.tabs, 4)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        central_widget.setMinimumSize(600, 400)
        self.setCentralWidget(central_widget)

    def show_toast(self, message, success=True, duration=3000):
        toast = ToastNotification(message, self, duration, success)
        toast.show_at_bottom_right(self)

    def update_status_bar(self, message=None, env=None, error=None):
        msg = []
        msg.append(message if message else "Ready")
        msg.append(f"Env: {env}" if env else "No environment selected")
        msg.append(f"Error: {error}" if error else "No errors")
        self.status_bar.showMessage(" | ".join(msg))

    def add_request_tab(self):
        from .request_tab import RequestTab
        from ..controllers.request_tab_controller import RequestTabController
        tab = RequestTab()
        RequestTabController(tab)
        self.tabs.addTab(tab, "New Request")
        tab.response_visualize.connect(self.send_to_response_visualizer)
        if hasattr(self, 'environment_manager_tab'):
            self.environment_manager_tab.environment_switched.connect(tab.set_env_vars)
        if hasattr(self, 'auth_tab'):
            self.auth_tab.auth_config_changed.connect(tab.set_auth_config)

    def add_gemini_tab(self):
        gemini_tab = QWidget()
        gemini_layout = QVBoxLayout()
        gemini_layout.setContentsMargins(0, 0, 0, 0)
        gemini_layout.setSpacing(0)
        gemini_webview = QWebEngineView()
        gemini_webview.setUrl("https://gemini.google.com/app")
        gemini_layout.addWidget(gemini_webview)
        gemini_tab.setLayout(gemini_layout)
        self.tabs.addTab(gemini_tab, "Gemini")

    def open_env_modal(self):
        self.env_modal.exec()

    def set_dark_theme(self):
        from PySide6.QtGui import QPalette, QColor
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

    def show_tab_context_menu(self, pos):
        index = self.tabs.tabBar().tabAt(pos)
        if index < 0:
            return
        menu = QMenu()
        close_action = menu.addAction("Close Tab")
        duplicate_action = menu.addAction("Duplicate Tab")
        quick_save_action = menu.addAction("Quick Save Tab Content")
        action = menu.exec(self.tabs.tabBar().mapToGlobal(pos))
        if action == close_action:
            self.close_tab(index)
        elif action == duplicate_action:
            tab_widget = self.tabs.widget(index)
            tab_type = self.tabs.tabText(index)
            if tab_type == "New Request":
                self.add_request_tab()
            elif tab_type == "History":
                self.add_history_tab()
            elif tab_type == "Gemini":
                self.add_gemini_tab()
        elif action == quick_save_action:
            tab_widget = self.tabs.widget(index)
            text = ""
            tab_type = self.tabs.tabText(index)
            edits = tab_widget.findChildren(QTextEdit)
            if edits:
                text = "\n---\n".join([e.toPlainText() for e in edits])
            elif tab_type == "Gemini":
                text = "Gemini tab content cannot be exported."
            else:
                text = "Tab content not available for export."
            filename, _ = QFileDialog.getSaveFileName(self, "Quick Save Tab Content", "tab_content.txt")
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(text)

    def add_history_tab(self):
        from ..controllers.history_controller import HistoryController
        from .history_tab import HistoryTab
        history_controller = HistoryController()
        tab = HistoryTab(history_controller.get_history())
        tab.request_rerun.connect(self.rerun_request_from_history)
        self.tabs.addTab(tab, "History")
        if hasattr(self, 'environment_manager_tab'):
            self.environment_manager_tab.environment_switched.connect(tab.set_env_vars)
        if hasattr(self, 'auth_tab'):
            self.auth_tab.auth_config_changed.connect(tab.set_auth_config)

    def rerun_request_from_history(self, entry):
        from .request_tab import RequestTab
        from ..controllers.request_tab_controller import RequestTabController
        tab = RequestTab()
        tab.method_box.setCurrentText(entry.get('method', 'GET'))
        tab.url_input.setText(entry.get('url', ''))
        tab.body_edit.setText(entry.get('response', ''))
        RequestTabController(tab)
        self.tabs.addTab(tab, f"Re-run: {entry.get('method', 'GET')}")

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def load_collection_request(self, req):
        from .request_tab import RequestTab
        from ..controllers.request_tab_controller import RequestTabController
        tab = RequestTab()
        tab.method_box.setCurrentText(req.get('method', 'GET'))
        tab.url_input.setText(req.get('url', ''))
        tab.body_edit.setText(req.get('body', ''))
        RequestTabController(tab)
        self.tabs.addTab(tab, f"Collection: {req.get('method', 'GET')}")


