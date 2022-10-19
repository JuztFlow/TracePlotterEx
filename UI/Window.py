from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

from UI.TestData import testData
from UI.MenuBar import MenuBar
from UI.TraceTable import TraceTable
from UI.TargetEdit import TargetEdit
from UI.PingGraph import PingGraph

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # UI setup
        self.setWindowTitle("Trace Plotter")
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(QVBoxLayout())

        # Add Menu
        self.setMenuBar(MenuBar())

        # Add target text box
        self.centralWidget().layout().addWidget(TargetEdit())

        # Add main graph
        traceTable = TraceTable()
        self.centralWidget().layout().addWidget(traceTable)
        for item in testData:
            traceTable.addRow(item)

        pingGraph = PingGraph("1.1.1.1")
        self.centralWidget().layout().addWidget(pingGraph)
        for index, item in enumerate(testData):
            pingGraph.addDataPoint(index, float(item["Avg"]))

        pingGraph = PingGraph("1.0.0.1")
        self.centralWidget().layout().addWidget(pingGraph)
        for index, item in enumerate(testData):
            pingGraph.addDataPoint(index, float(item["Avg"]))
