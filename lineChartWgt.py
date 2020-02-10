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
        if title == None:
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
        self.resize(800, 600)


    def updatePara(self, axisXRange=5, axisYRange=180,
                   axisXTickCount=11, axisYTickCount=11):
        self.axisXRange = axisXRange
        self.axisYRange = axisYRange
        self.axisXTickCount = axisXTickCount
        self.axisYTickCount = axisYTickCount
        self.axisXStep = self.axisXRange / (self.axisXTickCount - 1)
        self.axisYStep = self.axisYRange / (self.axisYTickCount - 1)


    def resizeEvent(self, event):
        # print("resize", self.min_x, self.min_y, self.max_y)
        super(lineChartWgt, self).resizeEvent(event)
        # 当窗口大小改变时需要重新计算
        # 坐标系中左上角顶点
        self.point_top = self._chart.mapToPosition(
            QPointF(self.min_x, self.max_y))
        # 坐标原点坐标
        self.point_bottom = self._chart.mapToPosition(
            QPointF(self.min_x, self.min_y))
        # print(self.point_top, self.point_bottom)


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
        self.initAxis()

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


    def initAxis(self):
        self.updatePara()
        self.axisX.setRange(0, self.axisXRange)  # 设置x轴范围
        self.axisX.setTickCount(self.axisXTickCount)  # x轴设置刻度
        self.axisY.setRange(0, self.axisYRange)  # 设置y轴范围
        self.axisY.setTickCount(self.axisYTickCount)  # y轴设置刻度
        # 获取x和y轴的最小最大值
        self.min_x, self.max_x = self.axisX.min(), self.axisX.max()
        self.min_y, self.max_y = self.axisY.min(), self.axisY.max()


    def mouseMoveEvent(self, event):
        super(lineChartWgt, self).mouseMoveEvent(event)

        mousePos = event.pos()
        # 把鼠标位置所在点转换为对应的xy值, xy为在chart中的坐标值
        x = self._chart.mapToValue(mousePos).x()
        y = self._chart.mapToValue(mousePos).y()
        points = []
        if self.dataX:
            for index, data_x in enumerate(self.dataX):
                if data_x >= x:
                    break
            if  index != 0:
                a = x-self.dataX[index-1]
                b = self.dataX[index]-x
                if a < b:
                    index -= 1
            # 得到在坐标系中的所有正常显示的series的类型和点
            # print(index)
            for serie in self._chart.series():
                point = serie.at(index)
                if abs(point.x()-x)<self.axisXStep and \
                      abs(point.y()-y)<self.axisYStep and \
                      self.min_x <= x <= self.max_x and \
                      self.min_y <= y <= self.max_y:
                    points.append((serie, point))

        if points:
            pos = self._chart.mapToPosition(point)
            self.lineItem.setLine(pos.x(), self.point_top.y(),
                                  pos.x(), self.point_bottom.y())
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


    def add_angle(self, curTime: int, curAngle: float) -> bool:
        '''
        接口函数，接收一个新角度，并进行绘图
        供主程序调用，传入时间和角度，进行绘图，返回接收成功
        '''
        if curTime > self.axisXRange:
            max_x = (curTime // self.axisXStep + 1) * self.axisXStep
            if max_x > self.max_x:
                self.max_x = max_x
                self.min_x = max_x-self.axisXRange
                self.axisX.setRange(self.min_x, self.max_x)
        self.serie.append(curTime, curAngle)
        self.dataX.append(curTime)
        # print(self.dataX)
        return True


    def clearSeries(self):
        for serie in self._chart.series():
            serie.clear()
        self.dataX = []
        self.initAxis()


if __name__ == '__main__':
    import sys
    from random import randint
    import time


    # 调用示例
    class WindowClass(QWidget):
        def __init__(self):
            super().__init__()
            layout=QVBoxLayout()
            self.chart = lineChartWgt()
            # self.resize(500,500)
            self.chart.setMinimumSize(800, 600)
            layout.addWidget(self.chart)

            self.btn = QPushButton()
            self.btn.setText("添加")
            self.btn.clicked.connect(self.add)
            layout.addWidget(self.btn)
            self.btn1 = QPushButton()
            self.btn1.setText("清空")
            self.btn1.clicked.connect(self.clear)
            layout.addWidget(self.btn1)
            self.setLayout(layout)

            self.t_start = time.time()

        def add(self):
            flag = self.chart.add_angle(time.time()-self.t_start, randint(80, 120))
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
