from cgitb import text
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, \
    QGraphicsItemGroup, QGraphicsRectItem, QGraphicsLineItem, QGraphicsTextItem
from PySide6.QtGui import QPen, QColor, QFont
from PySide6.QtCore import Qt

class CandlestickView(QGraphicsView):

    def __init__(self, height):
        super().__init__()
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.stickCount = 0
        self.stickWidth = self.width()
        self.stickHeight = height
        self.lastStick = None
        self.setScene(QGraphicsScene())

    def addStick(self, data):
        self.stickCount += 1

        candlestick = Candlestick(data, self.stickWidth, self.stickHeight, 10)

        # Add candlestick to graphicsview
        self.scene().addItem(candlestick)

        this_height = self.stickHeight * (self.stickCount - 1)
        last_height = self.stickHeight * (self.stickCount - 0)

        if self.lastStick:
            link = QGraphicsLineItem(self.lastStick.hookTo[0], candlestick.hookTo[1]+this_height, candlestick.hookTo[0], self.lastStick.hookTo[1]+last_height)
            link.setPen(QPen(QColor("red")))
            self.scene().addItem(link)

        # Move candlestick into position
        height = self.stickHeight * self.stickCount
        candlestick.moveBy(0, height)
        self.lastStick = candlestick

    def scrollContentsBy(self, x, y):
        pass


class Candlestick(QGraphicsItemGroup):

    def __init__(self, data, width, height, modifier):
        super().__init__()
        min = data["Min"] * modifier
        max = data["Max"] * modifier
        cur = data["Cur"] * modifier
        avg = data["Avg"] * modifier
        self.__hookAvg = (avg, height/2)

        # Set color
        backround = QGraphicsRectItem(1, 1, width, height)

        if data["Avg"] < 100:
            backround.setBrush(QColor(204, 255, 204))
        elif data["Avg"] < 200:
            backround.setBrush(QColor(255, 255, 204))
        else:
            backround.setBrush(QColor(255, 204, 204))


        self.addToGroup(backround)

        #Max To Min Bar
        self.addToGroup(QGraphicsLineItem(min, height/2, max, height/2))

        # Min Bar
        textItem = QGraphicsTextItem(str(data["Min"]))
        times = QFont("Times", 8)
        textItem.setFont(times)
        textItem.setPos(min - 30, height/3)
        self.addToGroup(textItem)
        self.addToGroup(QGraphicsLineItem(min, 10, min, height-10))

        # Max Bar
        textItem = QGraphicsTextItem(str(data["Max"]))
        times = QFont("Times", 8)
        textItem.setFont(times)
        textItem.setPos(max + 10, height/3)
        self.addToGroup(textItem)
        self.addToGroup(QGraphicsLineItem(max, 10, max, height-10))
        
        item = QGraphicsEllipseItem(avg-5, (height/2)-5, 10, 10)
        item.setPen(QPen(QColor("red")))
        self.addToGroup(item)
        
        # Avg Bar
        x_offset = cur-5
        y_offset = (height/2)
        topLeft     = (x_offset, y_offset-5)
        bottomRight = (10+x_offset, y_offset+5)
        bottomLeft  = (x_offset, y_offset+5)
        topRight    = (10+x_offset, y_offset-5)
        item = QGraphicsLineItem(topLeft[0], topLeft[1], bottomRight[0], bottomRight[1])
        item.setPen(QPen(QColor("blue")))
        self.addToGroup(item)
        item = QGraphicsLineItem(bottomLeft[0], bottomLeft[1], topRight[0], topRight[1])
        item.setPen(QPen(QColor("blue")))
        self.addToGroup(item)

    @property
    def hookTo(self):
        return self.__hookAvg
