from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QFormLayout

class EnvironmentModal(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Environment")
        layout = QVBoxLayout()
        form = QFormLayout()
        self.name_input = QLineEdit()
        form.addRow("Name:", self.name_input)
        self.vars_input = QLineEdit()
        form.addRow("Variables (key1=value1;key2=value2):", self.vars_input)
        layout.addLayout(form)
        self.add_btn = QPushButton("Add")
        layout.addWidget(self.add_btn)
        self.setLayout(layout)
