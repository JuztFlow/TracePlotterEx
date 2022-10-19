#!/usr/bin/python
# -*- coding: utf-8 -*-

from Server.Process import trace_to_db

import sys
from PySide6.QtWidgets import QApplication
from Client.Window import MainWindow

if __name__ == '__main__':
    
    # Server Test
    trace_to_db("sau53.org")

    # Client Test
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
