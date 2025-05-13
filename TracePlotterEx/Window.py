from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from TracePlotterEx.TestData import testData
from TracePlotterEx.MenuBar import MenuBar
from TracePlotterEx.TraceTable import TraceTable
from TracePlotterEx.TargetEdit import TargetEdit
from TracePlotterEx.PingGraph import PingGraph


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # UI setup
        self.setWindowTitle("TracePlotterEx")
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
