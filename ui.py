# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(997, 686)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabWidgetPage1 = QtWidgets.QWidget()
        self.tabWidgetPage1.setObjectName("tabWidgetPage1")
        self.gridLayout = QtWidgets.QGridLayout(self.tabWidgetPage1)
        self.gridLayout.setObjectName("gridLayout")
        self.lab_staticMeas = QtWidgets.QLabel(self.tabWidgetPage1)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lab_staticMeas.setFont(font)
        self.lab_staticMeas.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_staticMeas.setObjectName("lab_staticMeas")
        self.gridLayout.addWidget(self.lab_staticMeas, 3, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lcdnum_dist1 = QtWidgets.QLCDNumber(self.tabWidgetPage1)
        self.lcdnum_dist1.setSmallDecimalPoint(True)
        self.lcdnum_dist1.setDigitCount(7)
        self.lcdnum_dist1.setObjectName("lcdnum_dist1")
        self.horizontalLayout.addWidget(self.lcdnum_dist1)
        self.lcdnum_dist2 = QtWidgets.QLCDNumber(self.tabWidgetPage1)
        self.lcdnum_dist2.setSmallDecimalPoint(True)
        self.lcdnum_dist2.setDigitCount(7)
        self.lcdnum_dist2.setObjectName("lcdnum_dist2")
        self.horizontalLayout.addWidget(self.lcdnum_dist2)
        self.lcdnum_dist3 = QtWidgets.QLCDNumber(self.tabWidgetPage1)
        self.lcdnum_dist3.setSmallDecimalPoint(True)
        self.lcdnum_dist3.setDigitCount(7)
        self.lcdnum_dist3.setObjectName("lcdnum_dist3")
        self.horizontalLayout.addWidget(self.lcdnum_dist3)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.lineChartWgt = lineChartWgt(self.tabWidgetPage1)
        self.lineChartWgt.setObjectName("lineChartWgt")
        self.gridLayout.addWidget(self.lineChartWgt, 6, 0, 1, 1)
        self.lcdnum_staticMeas = QtWidgets.QLCDNumber(self.tabWidgetPage1)
        self.lcdnum_staticMeas.setSmallDecimalPoint(True)
        self.lcdnum_staticMeas.setDigitCount(7)
        self.lcdnum_staticMeas.setObjectName("lcdnum_staticMeas")
        self.gridLayout.addWidget(self.lcdnum_staticMeas, 4, 0, 1, 1)
        self.lab_dist = QtWidgets.QLabel(self.tabWidgetPage1)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lab_dist.setFont(font)
        self.lab_dist.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_dist.setObjectName("lab_dist")
        self.gridLayout.addWidget(self.lab_dist, 0, 0, 1, 1)
        self.lab_dynaMeas = QtWidgets.QLabel(self.tabWidgetPage1)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lab_dynaMeas.setFont(font)
        self.lab_dynaMeas.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_dynaMeas.setObjectName("lab_dynaMeas")
        self.gridLayout.addWidget(self.lab_dynaMeas, 5, 0, 1, 1)
        self.ShowColor = ShowColor(self.tabWidgetPage1)
        self.ShowColor.setObjectName("ShowColor")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.ShowColor)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_laser_1 = QtWidgets.QPushButton(self.ShowColor)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_laser_1.setFont(font)
        self.btn_laser_1.setCheckable(True)
        self.btn_laser_1.setObjectName("btn_laser_1")
        self.horizontalLayout_5.addWidget(self.btn_laser_1)
        self.btn_laser_2 = QtWidgets.QPushButton(self.ShowColor)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_laser_2.setFont(font)
        self.btn_laser_2.setCheckable(True)
        self.btn_laser_2.setObjectName("btn_laser_2")
        self.horizontalLayout_5.addWidget(self.btn_laser_2)
        self.btn_laser_3 = QtWidgets.QPushButton(self.ShowColor)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_laser_3.setFont(font)
        self.btn_laser_3.setCheckable(True)
        self.btn_laser_3.setObjectName("btn_laser_3")
        self.horizontalLayout_5.addWidget(self.btn_laser_3)
        self.gridLayout.addWidget(self.ShowColor, 2, 0, 1, 1)
        self.gridLayout.setRowStretch(0, 5)
        self.gridLayout.setRowStretch(1, 10)
        self.gridLayout.setRowStretch(2, 10)
        self.gridLayout.setRowStretch(3, 5)
        self.gridLayout.setRowStretch(4, 10)
        self.gridLayout.setRowStretch(5, 5)
        self.gridLayout.setRowStretch(6, 60)
        self.tabWidget_2.addTab(self.tabWidgetPage1, "")
        self.horizontalLayout_3.addWidget(self.tabWidget_2)
        self.tabWidget_1 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_1.setObjectName("tabWidget_1")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.lab_portNum_1 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lab_portNum_1.setFont(font)
        self.lab_portNum_1.setObjectName("lab_portNum_1")
        self.horizontalLayout_1.addWidget(self.lab_portNum_1)
        self.spinbox_portNum_1 = QtWidgets.QSpinBox(self.tab)
        self.spinbox_portNum_1.setProperty("value", 3)
        self.spinbox_portNum_1.setObjectName("spinbox_portNum_1")
        self.horizontalLayout_1.addWidget(self.spinbox_portNum_1)
        self.verticalLayout.addLayout(self.horizontalLayout_1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lab_portNum_2 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lab_portNum_2.setFont(font)
        self.lab_portNum_2.setObjectName("lab_portNum_2")
        self.horizontalLayout_2.addWidget(self.lab_portNum_2)
        self.spinbox_portNum_2 = QtWidgets.QSpinBox(self.tab)
        self.spinbox_portNum_2.setProperty("value", 4)
        self.spinbox_portNum_2.setObjectName("spinbox_portNum_2")
        self.horizontalLayout_2.addWidget(self.spinbox_portNum_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lab_portNum_3 = QtWidgets.QLabel(self.tab)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lab_portNum_3.setFont(font)
        self.lab_portNum_3.setObjectName("lab_portNum_3")
        self.horizontalLayout_4.addWidget(self.lab_portNum_3)
        self.spinbox_portNum_3 = QtWidgets.QSpinBox(self.tab)
        self.spinbox_portNum_3.setProperty("value", 5)
        self.spinbox_portNum_3.setObjectName("spinbox_portNum_3")
        self.horizontalLayout_4.addWidget(self.spinbox_portNum_3)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.btn_open = QtWidgets.QPushButton(self.tab)
        self.btn_open.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_open.setFont(font)
        self.btn_open.setCheckable(False)
        self.btn_open.setObjectName("btn_open")
        self.verticalLayout.addWidget(self.btn_open)
        self.btn_close = QtWidgets.QPushButton(self.tab)
        self.btn_close.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_close.setFont(font)
        self.btn_close.setCheckable(False)
        self.btn_close.setObjectName("btn_close")
        self.verticalLayout.addWidget(self.btn_close)
        self.btn_axis = QtWidgets.QPushButton(self.tab)
        self.btn_axis.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_axis.setFont(font)
        self.btn_axis.setObjectName("btn_axis")
        self.verticalLayout.addWidget(self.btn_axis)
        self.btn_zero = QtWidgets.QPushButton(self.tab)
        self.btn_zero.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_zero.setFont(font)
        self.btn_zero.setObjectName("btn_zero")
        self.verticalLayout.addWidget(self.btn_zero)
        self.btn_staticMeas = QtWidgets.QPushButton(self.tab)
        self.btn_staticMeas.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_staticMeas.setFont(font)
        self.btn_staticMeas.setObjectName("btn_staticMeas")
        self.verticalLayout.addWidget(self.btn_staticMeas)
        self.btn_dynaMeas = QtWidgets.QPushButton(self.tab)
        self.btn_dynaMeas.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_dynaMeas.setFont(font)
        self.btn_dynaMeas.setCheckable(True)
        self.btn_dynaMeas.setObjectName("btn_dynaMeas")
        self.verticalLayout.addWidget(self.btn_dynaMeas)
        self.checkbox_save = QtWidgets.QCheckBox(self.tab)
        self.checkbox_save.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.checkbox_save.setFont(font)
        self.checkbox_save.setObjectName("checkbox_save")
        self.verticalLayout.addWidget(self.checkbox_save)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.tabWidget_1.addTab(self.tab, "")
        self.horizontalLayout_3.addWidget(self.tabWidget_1)
        self.horizontalLayout_3.setStretch(0, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 997, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget_1.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "角度测量"))
        self.lab_staticMeas.setText(_translate("MainWindow", "静态测量结果：角度/°"))
        self.lab_dist.setText(_translate("MainWindow", "激光器读数：距离/mm"))
        self.lab_dynaMeas.setText(_translate("MainWindow", "动态测量结果"))
        self.btn_laser_1.setText(_translate("MainWindow", "1号端口"))
        self.btn_laser_2.setText(_translate("MainWindow", "2号端口"))
        self.btn_laser_3.setText(_translate("MainWindow", "3号端口"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabWidgetPage1), _translate("MainWindow", "结果"))
        self.lab_portNum_1.setText(_translate("MainWindow", "1号端口"))
        self.lab_portNum_2.setText(_translate("MainWindow", "2号端口"))
        self.lab_portNum_3.setText(_translate("MainWindow", "3号端口"))
        self.btn_open.setText(_translate("MainWindow", "连接设备"))
        self.btn_close.setText(_translate("MainWindow", "关闭设备"))
        self.btn_axis.setText(_translate("MainWindow", "旋转轴标定"))
        self.btn_zero.setText(_translate("MainWindow", "零位确定"))
        self.btn_staticMeas.setText(_translate("MainWindow", "静态测量"))
        self.btn_dynaMeas.setText(_translate("MainWindow", "动态测量"))
        self.checkbox_save.setText(_translate("MainWindow", "保存至文件"))
        self.tabWidget_1.setTabText(self.tabWidget_1.indexOf(self.tab), _translate("MainWindow", "控制"))
from AngleMeasurement import ShowColor
from lineChartWgt import lineChartWgt
