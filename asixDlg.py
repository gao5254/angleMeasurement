# -*- coding: utf-8 -*-


from PyQt5.QtCore import pyqtSignal, QRect, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QDialog, QListWidget, QPushButton, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QApplication


class axisDlg(QDialog):
    # 需要外界传入距离的信号
    distancesNeeded = pyqtSignal()
    # 数据采集完成的信号,传出采集到的距离的*二维列表*
    gatherFinished = pyqtSignal(list)

    # #声明无参数的信号
    # signal1 = pyqtSignal()
    # #声明带一个int类型参数的信号
    # signal2 = pyqtSignal(int)
    # #声明带int和str类型参数的信号
    # signal3 = pyqtSignal(int,str)
    # #声明带一个列表类型参数的信号
    # signal4 = pyqtSignal(list)
    # #声明带一个字典类型参数的信号
    # signal5 = pyqtSignal(dict)
    # #声明一个多重载版本的信号，包括带int和str类型参数的信号和带str类型参数的信号
    # signal6 = pyqtSignal([int,str], [str])
    # self.signal1.emit()
    # self.signal2.emit(1)
    # self.signal3.emit(1,"text")
    # self.signal4.emit([1,2,3,4])
    # self.signal5.emit({"name":"wangwu","age":"25"})
    # self.signal6[int,str].emit(1,"text")
    # self.signal6[str].emit("text")

    def __init__(self, parent=None):
        super(axisDlg, self).__init__(parent)
        self.setupUi()
        self.points = []

    def setupUi(self):
        self.setObjectName("axisDlg")
        self.setMinimumSize(410, 330)
        # self.resize(410, 330)

        self.HLayout = QHBoxLayout()
        self.VLayout = QVBoxLayout()

        self.listWidget = QListWidget(self)
        # self.listWidget.setGeometry(QRect(10, 10, 280, 260))
        self.listWidget.setObjectName("listView")
        self.HLayout.addWidget(self.listWidget)
        self.HLayout.addSpacing(15)

        self.addButton = QPushButton(self)
        # self.addButton.setGeometry(QRect(305, 30, 93, 28))
        self.addButton.setObjectName("addButton")
        self.addButton.clicked.connect(self.add)
        self.VLayout.addWidget(self.addButton)

        self.deleteButton = QPushButton(self)
        # self.deleteButton.setGeometry(QRect(305, 80, 93, 28))
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.clicked.connect(self.delete)
        self.VLayout.addWidget(self.deleteButton)

        self.clearButton = QPushButton(self)
        # self.clearButton.setGeometry(QRect(305, 130, 93, 28))
        self.clearButton.setObjectName("clearButton")
        self.clearButton.clicked.connect(self.clear)
        self.VLayout.addWidget(self.clearButton)

        self.okButton = QPushButton(self)
        # self.okButton.setGeometry(QRect(90, 290, 93, 28))
        self.okButton.setObjectName("okButton")
        self.okButton.clicked.connect(self.finish)
        self.VLayout.addWidget(self.okButton)

        self.cancelButton = QPushButton(self)
        # self.cancelButton.setGeometry(QRect(240, 290, 93, 28))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(self.cancel)
        self.VLayout.addWidget(self.cancelButton)

        self.HLayout.addLayout(self.VLayout)
        self.HLayout.addSpacing(5)
        self.setLayout(self.HLayout)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("axisDlg", "旋转轴标定"))
        self.addButton.setText(_translate("axisDlg", "添加"))
        self.deleteButton.setText(_translate("axisDlg", "删除"))
        self.clearButton.setText(_translate("axisDlg", "清空"))
        self.okButton.setText(_translate("axisDlg", "确定"))
        self.cancelButton.setText(_translate("axisDlg", "取消"))

    def add(self):
        # print("distancesNeeded")
        self.distancesNeeded.emit()

    def delete(self):
        item = self.listWidget.currentItem()
        row = self.listWidget.row(item)
        if row > -1:
            # print("删除第{}个".format(row+1))
            self.listWidget.takeItem(row)
            self.points.pop(row)
        # print(self.points)

    def clear(self):
        self.listWidget.clear()
        self.points.clear()

    def cancel(self):
        self.close()

    def set_distances(self, distances: list) -> bool:
        '''
        接口函数，接受距离列表
        供主程序调用，传入距离列表，显示并记录在类内部，返回设置成功
        '''
        string = "{:>10.4f}, {:>10.4f}, {:>10.4f}".format(distances[0], distances[1], distances[2])
        self.points.append(distances)
        self.listWidget.addItem(string)
        # print(self.points)

    def finish(self):
        # print("gatherFinished")
        if len(self.points) < 4:
            reply = QMessageBox.warning(self, "警告", "数据少于三个。", QMessageBox.Close, QMessageBox.Close)
        else:
            self.gatherFinished.emit(self.points)
            self.close()


if __name__ == '__main__':
    import sys
    from random import random

    # 调用示例
    class WindowClass(QWidget):
        def __init__(self):
            super().__init__()
            layout = QVBoxLayout()
            self.btn = QPushButton()
            self.btn.setText("打开对话框")
            self.btn.clicked.connect(self.showDialog)
            self.resize(500, 500)
            layout.addWidget(self.btn)
            self.setLayout(layout)

        def showDialog(self):
            self.dialog = axisDlg()
            self.dialog.show()
            self.dialog.distancesNeeded.connect(self.set_distances)
            self.dialog.gatherFinished.connect(self.finished)

        def set_distances(self):
            print("distancesNeeded")
            self.dialog.set_distances([random(), random(), random()])

        def finished(self, alist):
            print("gatherFinished")
            print(alist)

    try:
        app = QApplication(sys.argv)
        win = WindowClass()
        win.show()
        sys.exit(app.exec_())
    finally:
        del app
