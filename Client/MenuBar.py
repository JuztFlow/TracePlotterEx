
from PySide6.QtWidgets import QMenuBar
from PySide6.QtGui import QAction


class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()
        fileMenu = self.addMenu("File")
        fileMenu.addAction("New")

        save = QAction("Save",self)
        save.setShortcut("Ctrl+S")
        fileMenu.addAction(save)

        quit = QAction("Quit",self)
        quit.setShortcut("Ctrl+Q")
        fileMenu.addAction(quit)

        # Edit menu
        editMenu = self.addMenu("Edit")
        editMenu.addAction("Copy")
        editMenu.addAction("Paste")