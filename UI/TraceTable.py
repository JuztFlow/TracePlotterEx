from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QComboBox, QHeaderView

from UI.Candlestick import CandlestickView

class TraceTable(QTableWidget):
    def __init__(self):
        super().__init__()
        self.candlestickView = CandlestickView(30)

        self.setColumnCount(10)
        self.verticalHeader().setVisible(False)
        self.setHorizontalHeaderLabels(["Hop", "Count", "IP", "DNS", "Avg (O)", "Min", "Cur (X)", "Max", "Loss", "Candlestick"])

    def addRow(self, data):
        comboBox = QComboBox()
        for item in data["IP"]:
            comboBox.addItem(item)
        self.setRowCount(self.rowCount()+1)
        self.setItem(self.rowCount()-1,0, QTableWidgetItem(str(data["Hop"])))
        self.setItem(self.rowCount()-1,1, QTableWidgetItem(str(data["Count"])))
        self.setCellWidget(self.rowCount()-1, 2, comboBox)
        self.setItem(self.rowCount()-1, 3, QTableWidgetItem(data["DNS"]))
        self.setItem(self.rowCount()-1, 4, QTableWidgetItem(str(data["Avg"])))
        self.setItem(self.rowCount()-1, 5, QTableWidgetItem(str(data["Min"])))
        self.setItem(self.rowCount()-1, 6, QTableWidgetItem(str(data["Max"])))
        self.setItem(self.rowCount()-1, 7, QTableWidgetItem(str(data["Min"])))
        self.setItem(self.rowCount()-1, 8, QTableWidgetItem(data["Loss"]))

        # Add the candlestickView
        self.setSpan(0, 9, self.rowCount(), 10)
        self.setCellWidget(self.rowCount()-1, 9, self.candlestickView)
        self.candlestickView.addStick(data)

        # Update cell sizes...
        header = self.horizontalHeader()    
        for row in range(self.rowCount()-1):
            header.setSectionResizeMode(row, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(self.rowCount(), QHeaderView.Stretch)