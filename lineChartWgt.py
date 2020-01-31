# -*- coding: utf-8 -*-


from PyQt5 import QtWidgets
from PyQt5.QtChart import QChartView, QLineSeries, QChart
from PyQt5.QtGui import QPainter


class lineChartWgt(QChartView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.initChart()

    def initChart(self):
        self._chart = QChart(title="折线图堆叠")
        self._chart.setAcceptHoverEvents(True)
        # Series动画
        self._chart.setAnimationOptions(QChart.SeriesAnimations)

        self.series = QLineSeries(self._chart)
        self.series.append(0, 6)
        self.series.append(2, 4)
        self._chart.addSeries(self.series)
        self._chart.createDefaultAxes()  # 创建默认轴

        self.setChart(self._chart)


    def add_angle(self, curTime: int, curAngle: float) -> bool:
        '''
        接口函数，接收一个新角度，并进行绘图
        供主程序调用，传入时间和角度，进行绘图，返回接收成功
        '''
        pass


if __name__ == '__main__':
    import sys

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
            self.chart.series.append(1, 5.5)

    try:
        app=QtWidgets.QApplication(sys.argv)
        win=WindowClass()
        win.show()
        sys.exit(app.exec_())
    finally:
        del app
