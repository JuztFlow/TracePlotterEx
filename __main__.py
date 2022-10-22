#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PySide6.QtWidgets import QApplication

from Server.Networking import *
from Client.Window import MainWindow

if __name__ == '__main__':
    
    # Server Test
    if host_alive("sau53.org"):
        for hop in traceroute("sau53.org"):
            print(hop)
    # Client Test
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    
