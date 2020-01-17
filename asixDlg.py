# -*- coding: utf-8 -*-


import sys
from PyQt5 import QtCore, QtWidgets


class axisDlg(QtWidgets.QDialog):
    # 需要外界传入距离的信号
    distancesNeeded = QtCore.pyqtSignal()
    # 数据采集完成的信号,传出采集到的距离的*二维列表*
    gatherFinished = QtCore.pyqtSignal(list)

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

    def __init__(self):
        super().__init__()
        self.setupUi()
        # self.exec_()
        # self.show()

    def setupUi(self):
        self.setObjectName("axisDlg")
        self.resize(500, 350)
        self.listView = QtWidgets.QListView(self)
        self.listView.setGeometry(QtCore.QRect(10, 10, 350, 250))
        self.listView.setObjectName("listView")

        self.addButton = QtWidgets.QPushButton(self)
        self.addButton.setGeometry(QtCore.QRect(380, 30, 93, 28))
        self.addButton.setObjectName("addButton")
        self.addButton.clicked.connect(self.add)

        self.deleteButton = QtWidgets.QPushButton(self)
        self.deleteButton.setGeometry(QtCore.QRect(380, 80, 93, 28))
        self.deleteButton.setObjectName("deleteButton")

        self.okButton = QtWidgets.QPushButton(self)
        self.okButton.setGeometry(QtCore.QRect(120, 290, 93, 28))
        self.okButton.setObjectName("okButton")
        self.okButton.clicked.connect(self.accept)

        self.cancelButton = QtWidgets.QPushButton(self)
        self.cancelButton.setGeometry(QtCore.QRect(270, 290, 93, 28))
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(self.cancel)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("axisDlg", "旋转轴标定"))
        self.addButton.setText(_translate("axisDlg", "添加"))
        self.deleteButton.setText(_translate("axisDlg", "删除"))
        self.okButton.setText(_translate("axisDlg", "确定"))
        self.cancelButton.setText(_translate("axisDlg", "取消"))

    def add(self):
        self.distancesNeeded.emit()

    def cancel(self):
        self.close()


if __name__ == '__main__':

    # 调用示例
    class WindowClass(QtWidgets.QWidget):
        def __init__(self):
            super().__init__()
            layout=QtWidgets.QVBoxLayout()
            self.btn=QtWidgets.QPushButton()
            self.btn.setText("打开对话框")
            self.btn.clicked.connect(self.showDialog)
            self.resize(500,500)
            layout.addWidget(self.btn)
            self.setLayout(layout)

        def showDialog(self):
            self.dialog = axisDlg()
            self.dialog.show()
            self.dialog.distancesNeeded.connect(self.add)

        def add(self):
            print("distancesNeeded")


    try:
        app=QtWidgets.QApplication(sys.argv)
        win=WindowClass()
        win.show()
        sys.exit(app.exec_())
    finally:
        del app


    # try:
    #     app = QtWidgets.QApplication(sys.argv)
    #     dlg = axisDlg()
    #     dlg.show()
    #     sys.exit(app.exec_())
    # finally:
    #     del app
