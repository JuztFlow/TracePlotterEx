from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QLineEdit


class TargetEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QHBoxLayout())

        self.layout().addWidget(QLabel("Target:"))

        host = QLineEdit()
        self.layout().addWidget(host)
