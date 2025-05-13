import sys
from PySide6.QtWidgets import QApplication
from TracePlotterEx import target_alive, traceroute, ping
from TracePlotterEx import MainWindow

if __name__ == "__main__":

    # Test 1
    if target_alive("sau53.org"):
        for hop in traceroute("sau53.org"):
            print(hop)
        print(f" => Ping: {ping("sau53.org")}ms")

    print("")

    # Test 2
    if target_alive("141.95.72.160"):
        for hop in traceroute("141.95.72.160"):
            print(hop)
        print(f" => Ping: {ping("141.95.72.160")}ms")

    # Client Test
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
