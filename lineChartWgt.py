# -*- coding: utf-8 -*-


from PyQt5.QtChart import QChartView, QChart, QLineSeries
from PyQt5.QtCore import Qt, QPointF, QRectF, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QGraphicsLineItem, QWidget, \
    QHBoxLayout, QLabel, QVBoxLayout, QGraphicsProxyWidget, QPushButton


class ToolTipItem(QWidget):

    def __init__(self, color, text, parent=None):
        super(ToolTipItem, self).__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        clabel = QLabel(self)
        clabel.setMinimumSize(12, 12)
        clabel.setMaximumSize(12, 12)
        clabel.setStyleSheet("border-radius:6px;background: rgba(%s,%s,%s,%s);" % (
            color.red(), color.green(), color.blue(), color.alpha()))
        layout.addWidget(clabel)
        self.textLabel = QLabel(text, self, styleSheet="color:white;")
        layout.addWidget(self.textLabel)

    def setText(self, text):
        self.textLabel.setText(text)


class ToolTipWidget(QWidget):

    Cache = {}

    def __init__(self, *args, **kwargs):
        super(ToolTipWidget, self).__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            "ToolTipWidget{background: rgba(50, 50, 50, 100);}")
        layout = QVBoxLayout(self)
        self.titleLabel = QLabel(self, styleSheet="color:white;")
        layout.addWidget(self.titleLabel)

    def updateUi(self, title, points):
        if title is None:
            self.titleLabel.hide()
        else:
            self.titleLabel.setText(title)
        for serie, point in points:
            text = "{:.3f}, {:.3f}".format(point.x(), point.y())
            if serie not in self.Cache:
                item = ToolTipItem(serie.color(), text, self)
                self.layout().addWidget(item)
                self.Cache[serie] = item
            else:
                self.Cache[serie].setText(text)
            self.Cache[serie].setVisible(serie.isVisible())  # 隐藏那些不可用的项
        self.adjustSize()  # 调整大小


class GraphicsProxyWidget(QGraphicsProxyWidget):

    def __init__(self, *args, **kwargs):
        super(GraphicsProxyWidget, self).__init__(*args, **kwargs)
        self.setZValue(999)
        self.tipWidget = ToolTipWidget()
        self.setWidget(self.tipWidget)
        self.hide()

    def width(self):
        return self.size().width()

    def height(self):
        return self.size().height()

    def show(self, title, points, pos):
        self.setGeometry(QRectF(pos, self.size()))
        self.tipWidget.updateUi(title, points)
        super(GraphicsProxyWidget, self).show()


class lineChartWgt(QChartView):
    def __init__(self, parent=None):
        super(lineChartWgt, self).__init__(parent)
        self.initChart()
        self.dataX = []
        self.leftClicked = False

    def updateAxis(self, minX=0, axisXRange=5, minY=-5, axisYRange=10,
                   axisXTickCount=11, axisYTickCount=3):
        self.axisXRange = axisXRange
        self.axisYRange = axisYRange
        self.axisXTickCount = axisXTickCount
        self.axisYTickCount = axisYTickCount
        self.axisXStep = axisXRange / (axisXTickCount - 1)
        self.axisYStep = axisYRange / (axisYTickCount - 1)

        self.minX = minX
        self.maxX = minX + axisXRange
        self.minY = minY
        self.maxY = minY + axisYRange

        self.axisX.setRange(self.minX, self.maxX)  # 设置x轴范围
        self.axisX.setTickCount(self.axisXTickCount)  # x轴设置刻度
        self.axisY.setRange(self.minY, self.maxY)  # 设置y轴范围
        self.axisY.setTickCount(self.axisYTickCount)  # y轴设置刻度

        self.locate()

    def initChart(self):
        self._chart = QChart()
        self._chart.setAcceptHoverEvents(True)
        # Series动画
        # self._chart.setAnimationOptions(QChart.SeriesAnimations)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        self.serie = QLineSeries(self._chart)
        self.serie.setPointsVisible(True)  # 显示圆点
        self._chart.addSeries(self.serie)
        self.setChart(self._chart)

        self._chart.createDefaultAxes()  # 创建默认轴
        self.axisX, self.axisY = self._chart.axisX(), self._chart.axisY()
        self.axisX = self._chart.axisX()
        self.axisX.setTitleText("时间 / s")
        self.axisY = self._chart.axisY()
        self.axisY.setTitleText("角度 / °")
        self.updateAxis()

        # chart的图例
        legend = self._chart.legend()
        # 设置图例由Series来决定样式
        # legend.setMarkerShape(QLegend.MarkerShapeFromSeries)
        legend.hide()

        # 提示widget
        self.toolTipWidget = GraphicsProxyWidget(self._chart)
        # line
        self.lineItem = QGraphicsLineItem(self._chart)
        pen = QPen(Qt.gray)
        pen.setWidth(1)
        self.lineItem.setPen(pen)
        self.lineItem.setZValue(998)
        self.lineItem.hide()

    def add_angle(self, curTime: int, curAngle: float) -> bool:
        '''
        接口函数，接收一个新角度，并进行绘图
        供主程序调用，传入时间和角度，进行绘图，返回接收成功
        '''
        updateAxisFlag = False
        # if curTime > self.axisXRange:
        maxX = (curTime // self.axisXStep + 2) * self.axisXStep
        if maxX > self.maxX:
            # self.maxX = maxX
            self.minX = maxX - self.axisXRange
            # self.axisX.setRange(self.minX, self.maxX)
            updateAxisFlag = True

        if curAngle > 0:
            jumpStep = curAngle // self.axisYStep + 1
            maxY = jumpStep * self.axisYStep
            if maxY > self.maxY:
                self.axisYRange = maxY - self.minY
                self.axisYTickCount = int(self.axisYRange / self.axisYStep + 1)
                updateAxisFlag = True
        elif curAngle < 0:
            jumpStep = curAngle // self.axisYStep - (0 if curAngle % self.axisYStep != 0 else 1)
            minY = jumpStep * self.axisYStep
            if minY < self.minY:
                self.minY = minY
                self.axisYRange = self.maxY - minY
                self.axisYTickCount = int(self.axisYRange / self.axisYStep + 1)
                updateAxisFlag = True

        if updateAxisFlag:
            self.updateAxis(self.minX, self.axisXRange, self.minY, self.axisYRange, self.axisXTickCount, self.axisYTickCount)

        self.serie.append(curTime, curAngle)
        self.dataX.append(curTime)
        # print(self.dataX)
        return True

    def clearSeries(self):
        for serie in self._chart.series():
            serie.clear()
        self.dataX = []
        self.updateAxis()

    def resizeEvent(self, event):
        super(lineChartWgt, self).resizeEvent(event)
        # 当窗口大小改变时需要重新计算
        self.locate()

    def locate(self):
        self.pointLeftTop = self._chart.mapToPosition(
            QPointF(self.minX, self.maxY))
        self.pointLeftBottom = self._chart.mapToPosition(
            QPointF(self.minX, self.minY))
        self.pointRightBottom = self._chart.mapToPosition(
            QPointF(self.maxX, self.minY))
        self.xValuePerPos = (self.maxX - self.minX) / \
            (self.pointRightBottom.x() - self.pointLeftBottom.x())
        self.yValuePerPos = (self.maxY - self.minY) / \
            (self.pointLeftTop.y() - self.pointLeftBottom.y())

    def searchIndex(self, arr, left, right, x):
        # 二分查找
        # 基本判断
        if right >= left:
            mid = int(left + (right - left) / 2)
            # 元素整好的中间位置
            if arr[mid] == x:
                return mid
            # 元素小于中间位置的元素，只需要再比较左边的元素
            elif arr[mid] > x:
                return self.searchIndex(arr, left, mid - 1, x)
            # 元素大于中间位置的元素，只需要再比较右边的元素
            else:
                return self.searchIndex(arr, mid + 1, right, x)
        else:
            # 不存在
            return left

    def mouseMoveEvent(self, event):
        super(lineChartWgt, self).mouseMoveEvent(event)
        # 把鼠标位置所在点转换为对应的xy值, xy为在chart中的坐标值
        valuePos = self._chart.mapToValue(event.pos())
        xValue = valuePos.x()
        yValue = valuePos.y()
        points = []
        if self.dataX:
            # 二分查找比xValue大的index
            index = self.searchIndex(self.dataX, 0, len(self.dataX) - 1, xValue)
            # for index, data_x in enumerate(self.dataX):
            #     if data_x >= xValue:
            #         break
            if index == len(self.dataX):
                index -= 1
            # 判断靠近左边还是右边的点
            if index != 0:
                a = xValue - self.dataX[index - 1]
                b = self.dataX[index] - xValue
                if a < b:
                    index -= 1
            # 得到在坐标系中的所有正常显示的series的类型和点
            for serie in self._chart.series():
                point = serie.at(index)
                # abs(point.y() - yValue) < self.axisYStep and \
                if abs(point.x() - xValue) < self.axisXStep and \
                    self.minX <= xValue <= self.maxX and \
                        self.minY <= yValue <= self.maxY:
                    points.append((serie, point))

        if points:
            pos = self._chart.mapToPosition(point)
            self.lineItem.setLine(pos.x(), self.pointLeftTop.y(),
                                  pos.x(), self.pointLeftBottom.y())
            self.lineItem.show()
            t_width = self.toolTipWidget.width()
            t_height = self.toolTipWidget.height()
            # 如果点位置离右侧的距离小于tip宽度
            temp_x = pos.x() - t_width if self.width() - \
                pos.x() - 20 < t_width else pos.x()
            # 如果鼠标位置离底部的高度小于tip高度
            temp_y = pos.y() - t_height if self.height() - \
                pos.y() - 20 < t_height else pos.y()
            self.toolTipWidget.show(None, points, QPoint(temp_x, temp_y))
        else:
            self.toolTipWidget.hide()
            self.lineItem.hide()

        if self.leftClicked:
            # print(event.pos())
            self._movePos = event.pos() - self._startPos
            self.minX -= (self._movePos.x() * self.xValuePerPos)
            self.maxX = self.minX + self.axisXRange
            self.minY -= (self._movePos.y() * self.yValuePerPos)
            self.maxY = self.minY + self.axisYRange
            self.axisX.setRange(self.minX, self.maxX)
            self.axisY.setRange(self.minY, self.maxY)
            self._startPos = event.pos()

    def mousePressEvent(self, event):
        super(lineChartWgt, self).mousePressEvent(event)
        if event.button() == Qt.LeftButton:
            self.leftClicked = True
            self._startPos = event.pos()
            # print("left", self.leftClicked)

    def mouseReleaseEvent(self, event):
        super(lineChartWgt, self).mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            self.leftClicked = False
            # print("left", self.leftClicked)

    def wheelEvent(self, event):
        super(lineChartWgt, self).wheelEvent(event)
        valuePos = self._chart.mapToValue(event.pos())
        xValue = valuePos.x()
        yValue = valuePos.y()
        if event.angleDelta().y() < 0:
            # 缩小，视野变大
            scale = 1.2
        else:
            # 放大，视野变小
            scale = 0.8

        self.axisXRange *= scale
        self.minX -= (xValue - self.minX) * (scale - 1)
        self.axisYRange *= scale
        self.minY -= (yValue - self.minY) * (scale - 1)

        self.updateAxis(minX=self.minX, axisXRange=self.axisXRange,
                        minY=self.minY, axisYRange=self.axisYRange,
                        axisXTickCount=11, axisYTickCount=11)


if __name__ == '__main__':
    import sys
    from random import randint
    import time
    from PyQt5.QtCore import QTimer

    # 调用示例

    class WindowClass(QWidget):
        def __init__(self):
            super().__init__()
            layout = QVBoxLayout()
            self.chart = lineChartWgt()
            # self.resize(500,500)
            self.chart.setMinimumSize(800, 600)
            layout.addWidget(self.chart)

            self.btnStart = QPushButton()
            self.btnStart.setText("开始")
            self.btnStart.clicked.connect(self.start)
            layout.addWidget(self.btnStart)

            self.btnPause = QPushButton()
            self.btnPause.setText("暂停")
            self.btnPause.clicked.connect(self.pause)
            layout.addWidget(self.btnPause)

            self.btnClear = QPushButton()
            self.btnClear.setText("清空")
            self.btnClear.clicked.connect(self.clear)
            layout.addWidget(self.btnClear)
            self.setLayout(layout)

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.add)

        def start(self):
            self.timer.start(100)
            self.t_start = time.time()

        def pause(self):
            self.timer.stop()

        def add(self):
            flag = self.chart.add_angle(
                time.time() - self.t_start, randint(-30, 30))
            print(flag)

        def clear(self):
            self.chart.clearSeries()
            self.t_start = time.time()

    try:
        app = QApplication(sys.argv)
        win = WindowClass()
        win.show()
        sys.exit(app.exec_())
    finally:
        del app
