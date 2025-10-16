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
    def show_toast(self, message, success=True, duration=3000):
        toast = ToastNotification(message, self, duration, success)
        toast.show_at_bottom_right(self)
    def send_to_response_visualizer(self, response_text):
        self.response_visualizer_tab.data_edit.setText(response_text)
        self.tabs.setCurrentWidget(self.response_visualizer_tab)
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SoulFetch API Client")
        self.setGeometry(100, 100, 1200, 800)
        self.set_dark_theme()

        # Privacy Mode
        self.privacy_mode = False
        self.privacy_btn = QPushButton("Privacy Mode: OFF")
        self.privacy_btn.setCheckable(True)
        self.privacy_btn.setStyleSheet("background: #444; color: #f1fa8c; border-radius: 6px; padding: 6px 18px;")
        self.privacy_btn.clicked.connect(self.toggle_privacy_mode)

        # Global Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready | No environment selected | No errors")

        self.status_bar.addPermanentWidget(self.privacy_btn)
        # Theme Selector
        from PySide6.QtWidgets import QComboBox
        self.theme_selector = QComboBox()
        self.theme_selector.addItems(["Dark", "Light"])
        self.theme_selector.setCurrentText("Dark")
        self.theme_selector.setStyleSheet("background: #222; color: #8be9fd; border-radius: 6px; padding: 6px 12px;")
        self.theme_selector.currentTextChanged.connect(self.change_theme)
        self.status_bar.addPermanentWidget(self.theme_selector)
    def change_theme(self, theme):
        from PySide6.QtGui import QPalette, QColor
        palette = QPalette()
        if theme == "Dark":
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
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor(245, 245, 245))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.Text, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.Button, QColor(230, 230, 230))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(30, 30, 30))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(180, 180, 180))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(30, 30, 30))
        self.setPalette(palette)
        self.show_toast(f"Theme changed to {theme} mode.", success=True)
    def toggle_privacy_mode(self):
        self.privacy_mode = not self.privacy_mode
        if self.privacy_mode:
            self.privacy_btn.setText("Privacy Mode: ON")
            self.status_bar.showMessage("Privacy Mode enabled | No history or persistence will be saved")
            self.show_toast("Privacy Mode enabled. History and persistence are disabled.", success=True)
        else:
            self.privacy_btn.setText("Privacy Mode: OFF")
            self.status_bar.showMessage("Privacy Mode disabled | History and persistence are active")
            self.show_toast("Privacy Mode disabled. History and persistence are active.", success=False)

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
        self.tabs.setMovable(True)  # Permite reordenar pestañas arrastrando
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.show_tab_context_menu)

        # Add New Request button above tab bar
        tabbar_layout = QVBoxLayout()
        self.new_request_btn = QPushButton("+ New Request")
        self.new_request_btn.setStyleSheet("font-weight: bold; background: #222; color: #8be9fd; border-radius: 6px; padding: 6px 18px;")
        self.new_request_btn.clicked.connect(self.add_request_tab)
        tabbar_layout.addWidget(self.new_request_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        tabbar_layout.addWidget(self.tabs)

        # Add tabs
        self.add_request_tab()
        self.add_history_tab()
        self.add_gemini_tab()
        # Add all feature tabs inside __init__
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
        # Advanced features tabs
        from .user_manager_tab import UserManagerTab
        self.user_manager_tab = UserManagerTab()
        self.tabs.addTab(self.user_manager_tab, "User Management")
        from .cloud_sync_tab import CloudSyncTab
        self.cloud_sync_tab = CloudSyncTab()
        self.tabs.addTab(self.cloud_sync_tab, "Cloud Sync")
        from .codegen_tab import CodeGenTab
        self.codegen_tab = CodeGenTab()
        self.tabs.addTab(self.codegen_tab, "CodeGen")
        from .accessibility_tab import AccessibilityTab
        self.accessibility_tab = AccessibilityTab()
        self.tabs.addTab(self.accessibility_tab, "Accessibility/i18n")
        from .visualization_tab import VisualizationTab
        self.visualization_tab = VisualizationTab()
        self.tabs.addTab(self.visualization_tab, "Visualization")

        # Layout: sidebar | tabs
        main_layout = QHBoxLayout()
        self.sidebar_widget.setMinimumWidth(220)
        self.sidebar_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # Use tabbar_layout instead of direct tabs
        tabbar_container = QWidget()
        tabbar_container.setLayout(tabbar_layout)
        tabbar_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.sidebar_widget, 1)
        main_layout.addWidget(tabbar_container, 4)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        central_widget.setMinimumSize(600, 400)
        self.setCentralWidget(central_widget)

        # Keyboard Shortcuts
        from PySide6.QtGui import QShortcut, QKeySequence
        send_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        send_shortcut.activated.connect(self.trigger_send_request)
        copy_shortcut = QShortcut(QKeySequence("Ctrl+Shift+C"), self)
        copy_shortcut.activated.connect(self.trigger_copy_response)
        next_tab_shortcut = QShortcut(QKeySequence("Ctrl+Tab"), self)
        next_tab_shortcut.activated.connect(self.next_tab)
        prev_tab_shortcut = QShortcut(QKeySequence("Ctrl+Shift+Tab"), self)
        prev_tab_shortcut.activated.connect(self.prev_tab)
    def trigger_send_request(self):
        tab = self.tabs.currentWidget()
        from .request_tab import RequestTab
        if isinstance(tab, RequestTab):
            tab.send_btn.click()
            self.show_toast("Request sent (Ctrl+Enter)", success=True)

    def trigger_copy_response(self):
        tab = self.tabs.currentWidget()
        from .request_tab import RequestTab
        if isinstance(tab, RequestTab):
            text = tab.response_pretty.toPlainText()
            from PySide6.QtWidgets import QApplication
            QApplication.clipboard().setText(text)
            self.show_toast("Response copied (Ctrl+Shift+C)", success=True)

    def next_tab(self):
        idx = self.tabs.currentIndex()
        count = self.tabs.count()
        self.tabs.setCurrentIndex((idx + 1) % count)

    def prev_tab(self):
        idx = self.tabs.currentIndex()
        count = self.tabs.count()
        self.tabs.setCurrentIndex((idx - 1) % count)

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
        # Prevent closing History tab
        tab_text = self.tabs.tabText(index)
        if tab_text == "History":
            self.show_toast("History tab cannot be closed.", success=False)
            return
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


