from PySide6.QtCharts import QChartView, QChart, QLineSeries
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt

class PingGraph(QChartView):
    def __init__(self, title):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)
        self.setChart(QChart()) 
        self.chart().addSeries(QLineSeries())
        self.chart().createDefaultAxes()
        self.chart().setAnimationOptions(QChart.SeriesAnimations)
        self.chart().setTitle(title)
        self.chart().legend().setVisible(True)
        self.chart().legend().setAlignment(Qt.AlignBottom)

    def addDataPoint(self, x, y):
        self.chart().series().append((x, y))