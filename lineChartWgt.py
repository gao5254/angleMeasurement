# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets
from PyQt5.QtChart import QChartView, QLineSeries, QChart
from PyQt5.QtGui import QPainter


class lineChartWgt(QChartView):
    def __init__(self):
        super().__init__()
        self.initChart()

    def initChart(self):
        self._chart = QChart(title="折线图堆叠")
        self._chart.setAcceptHoverEvents(True)
        # Series动画
        self._chart.setAnimationOptions(QChart.SeriesAnimations)

        self.series = QLineSeries(self._chart)
        self._chart.addSeries(self.series)
        self._chart.createDefaultAxes()  # 创建默认轴
        self.setChart(self._chart)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿

        self.axisX = self._chart.axisX()
        self.axisX.setRange(0, 20)  # 设置y轴范围
        self.axisY = self._chart.axisY()
        # axisY.setTickCount(7)  # y轴设置7个刻度
        self.axisY.setRange(0, 180)  # 设置y轴范围


    def add_angle(self, curTime: int, curAngle: float) -> bool:
        '''
        接口函数，接收一个新角度，并进行绘图
        供主程序调用，传入时间和角度，进行绘图，返回接收成功
        '''
        if curTime > 20:
            max_x = (curTime // 5 + 1) * 5
            self.axisX.setRange(max_x-20, max_x)
        self.series.append(curTime, curAngle)
        return True


if __name__ == '__main__':
    import sys
    from random import randint
    import time

    t_start = time.time()
    # 调用示例
    class WindowClass(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()
            layout=QtWidgets.QVBoxLayout()
            self.chart = lineChartWgt()
            # self.resize(500,500)
            self.chart.setMinimumSize(800, 600)
            layout.addWidget(self.chart)

            self.btn=QtWidgets.QPushButton()
            self.btn.setText("添加")
            self.btn.clicked.connect(self.add)
            layout.addWidget(self.btn)
            self.setLayout(layout)

        def add(self):
            flag = self.chart.add_angle(time.time()-t_start, randint(80, 120))

    try:
        app=QtWidgets.QApplication(sys.argv)
        win=WindowClass()
        win.show()
        sys.exit(app.exec_())
    finally:
        del app
