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
        font = QtGui.QFont()
        font.setPointSize(11)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabWidgetPage1 = QtWidgets.QWidget()
        self.tabWidgetPage1.setObjectName("tabWidgetPage1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tabWidgetPage1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lab_dist = QtWidgets.QLabel(self.tabWidgetPage1)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lab_dist.setFont(font)
        self.lab_dist.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_dist.setObjectName("lab_dist")
        self.verticalLayout_2.addWidget(self.lab_dist)
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
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.ShowColor = ShowColor(self.tabWidgetPage1)
        self.ShowColor.setEnabled(False)
        self.ShowColor.setObjectName("ShowColor")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.ShowColor)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_laser_1 = QtWidgets.QPushButton(self.ShowColor)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_laser_1.setFont(font)
        self.btn_laser_1.setCheckable(True)
        self.btn_laser_1.setObjectName("btn_laser_1")
        self.horizontalLayout_5.addWidget(self.btn_laser_1)
        self.btn_laser_2 = QtWidgets.QPushButton(self.ShowColor)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_laser_2.setFont(font)
        self.btn_laser_2.setCheckable(True)
        self.btn_laser_2.setObjectName("btn_laser_2")
        self.horizontalLayout_5.addWidget(self.btn_laser_2)
        self.btn_laser_3 = QtWidgets.QPushButton(self.ShowColor)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.btn_laser_3.setFont(font)
        self.btn_laser_3.setCheckable(True)
        self.btn_laser_3.setObjectName("btn_laser_3")
        self.horizontalLayout_5.addWidget(self.btn_laser_3)
        self.verticalLayout_2.addWidget(self.ShowColor)
        self.lab_staticMeas = QtWidgets.QLabel(self.tabWidgetPage1)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lab_staticMeas.setFont(font)
        self.lab_staticMeas.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_staticMeas.setObjectName("lab_staticMeas")
        self.verticalLayout_2.addWidget(self.lab_staticMeas)
        self.lcdnum_staticMeas = QtWidgets.QLCDNumber(self.tabWidgetPage1)
        self.lcdnum_staticMeas.setSmallDecimalPoint(True)
        self.lcdnum_staticMeas.setDigitCount(6)
        self.lcdnum_staticMeas.setObjectName("lcdnum_staticMeas")
        self.verticalLayout_2.addWidget(self.lcdnum_staticMeas)
        self.lab_dynaMeas = QtWidgets.QLabel(self.tabWidgetPage1)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lab_dynaMeas.setFont(font)
        self.lab_dynaMeas.setAlignment(QtCore.Qt.AlignCenter)
        self.lab_dynaMeas.setObjectName("lab_dynaMeas")
        self.verticalLayout_2.addWidget(self.lab_dynaMeas)
        self.lineChartWgt = lineChartWgt(self.tabWidgetPage1)
        self.lineChartWgt.setObjectName("lineChartWgt")
        self.verticalLayout_2.addWidget(self.lineChartWgt)
        self.verticalLayout_2.setStretch(0, 5)
        self.verticalLayout_2.setStretch(1, 10)
        self.verticalLayout_2.setStretch(2, 10)
        self.verticalLayout_2.setStretch(3, 5)
        self.verticalLayout_2.setStretch(4, 10)
        self.verticalLayout_2.setStretch(5, 5)
        self.verticalLayout_2.setStretch(6, 60)
        self.tabWidget_2.addTab(self.tabWidgetPage1, "")
        self.horizontalLayout_3.addWidget(self.tabWidget_2)
        self.tabWidget_1 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_1.setObjectName("tabWidget_1")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout_3.setSpacing(9)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.connectBox = QtWidgets.QGroupBox(self.tab)
        self.connectBox.setAlignment(QtCore.Qt.AlignCenter)
        self.connectBox.setFlat(True)
        self.connectBox.setObjectName("connectBox")
        self.gridLayout = QtWidgets.QGridLayout(self.connectBox)
        self.gridLayout.setObjectName("gridLayout")
        self.spinbox_portNum_1 = QtWidgets.QSpinBox(self.connectBox)
        self.spinbox_portNum_1.setProperty("value", 3)
        self.spinbox_portNum_1.setObjectName("spinbox_portNum_1")
        self.gridLayout.addWidget(self.spinbox_portNum_1, 1, 1, 1, 1)
        self.btn_close = QtWidgets.QPushButton(self.connectBox)
        self.btn_close.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_close.setFont(font)
        self.btn_close.setCheckable(False)
        self.btn_close.setObjectName("btn_close")
        self.gridLayout.addWidget(self.btn_close, 6, 0, 1, 2)
        self.lab_portNum_2 = QtWidgets.QLabel(self.connectBox)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lab_portNum_2.setFont(font)
        self.lab_portNum_2.setObjectName("lab_portNum_2")
        self.gridLayout.addWidget(self.lab_portNum_2, 2, 0, 1, 1)
        self.btn_open = QtWidgets.QPushButton(self.connectBox)
        self.btn_open.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_open.setFont(font)
        self.btn_open.setCheckable(False)
        self.btn_open.setObjectName("btn_open")
        self.gridLayout.addWidget(self.btn_open, 5, 0, 1, 2)
        self.lab_portNum_3 = QtWidgets.QLabel(self.connectBox)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lab_portNum_3.setFont(font)
        self.lab_portNum_3.setObjectName("lab_portNum_3")
        self.gridLayout.addWidget(self.lab_portNum_3, 3, 0, 1, 1)
        self.lab_portNum_1 = QtWidgets.QLabel(self.connectBox)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.lab_portNum_1.setFont(font)
        self.lab_portNum_1.setObjectName("lab_portNum_1")
        self.gridLayout.addWidget(self.lab_portNum_1, 1, 0, 1, 1)
        self.spinbox_portNum_2 = QtWidgets.QSpinBox(self.connectBox)
        self.spinbox_portNum_2.setProperty("value", 4)
        self.spinbox_portNum_2.setObjectName("spinbox_portNum_2")
        self.gridLayout.addWidget(self.spinbox_portNum_2, 2, 1, 1, 1)
        self.spinbox_portNum_3 = QtWidgets.QSpinBox(self.connectBox)
        self.spinbox_portNum_3.setProperty("value", 5)
        self.spinbox_portNum_3.setObjectName("spinbox_portNum_3")
        self.gridLayout.addWidget(self.spinbox_portNum_3, 3, 1, 1, 1)
        self.openProgressBar = QtWidgets.QProgressBar(self.connectBox)
        self.openProgressBar.setMaximum(3)
        self.openProgressBar.setProperty("value", 0)
        self.openProgressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.openProgressBar.setTextVisible(True)
        self.openProgressBar.setObjectName("openProgressBar")
        self.gridLayout.addWidget(self.openProgressBar, 0, 0, 1, 2)
        self.verticalLayout_3.addWidget(self.connectBox)
        self.paraBox = QtWidgets.QGroupBox(self.tab)
        self.paraBox.setEnabled(False)
        self.paraBox.setAlignment(QtCore.Qt.AlignCenter)
        self.paraBox.setFlat(True)
        self.paraBox.setObjectName("paraBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.paraBox)
        self.gridLayout_2.setHorizontalSpacing(3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.btn_axis = QtWidgets.QPushButton(self.paraBox)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_axis.setFont(font)
        self.btn_axis.setObjectName("btn_axis")
        self.gridLayout_2.addWidget(self.btn_axis, 0, 0, 1, 2)
        self.btn_zero = QtWidgets.QPushButton(self.paraBox)
        self.btn_zero.setEnabled(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_zero.setFont(font)
        self.btn_zero.setObjectName("btn_zero")
        self.gridLayout_2.addWidget(self.btn_zero, 1, 0, 1, 2)
        self.btn_readPara = QtWidgets.QPushButton(self.paraBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_readPara.setFont(font)
        self.btn_readPara.setObjectName("btn_readPara")
        self.gridLayout_2.addWidget(self.btn_readPara, 2, 0, 1, 1)
        self.btn_savePara = QtWidgets.QPushButton(self.paraBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btn_savePara.setFont(font)
        self.btn_savePara.setObjectName("btn_savePara")
        self.gridLayout_2.addWidget(self.btn_savePara, 2, 1, 1, 1)
        self.verticalLayout_3.addWidget(self.paraBox)
        self.measureBox = QtWidgets.QGroupBox(self.tab)
        self.measureBox.setEnabled(False)
        self.measureBox.setAlignment(QtCore.Qt.AlignCenter)
        self.measureBox.setFlat(True)
        self.measureBox.setObjectName("measureBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.measureBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btn_staticMeas = QtWidgets.QPushButton(self.measureBox)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_staticMeas.setFont(font)
        self.btn_staticMeas.setObjectName("btn_staticMeas")
        self.verticalLayout.addWidget(self.btn_staticMeas)
        self.btn_dynaMeas = QtWidgets.QPushButton(self.measureBox)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.btn_dynaMeas.setFont(font)
        self.btn_dynaMeas.setCheckable(True)
        self.btn_dynaMeas.setObjectName("btn_dynaMeas")
        self.verticalLayout.addWidget(self.btn_dynaMeas)
        self.checkbox_save = QtWidgets.QCheckBox(self.measureBox)
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
        self.verticalLayout_3.addWidget(self.measureBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.tabWidget_1.addTab(self.tab, "")
        self.horizontalLayout_3.addWidget(self.tabWidget_1)
        self.horizontalLayout_3.setStretch(0, 9)
        self.horizontalLayout_3.setStretch(1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 997, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget_1.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.spinbox_portNum_1, self.spinbox_portNum_2)
        MainWindow.setTabOrder(self.spinbox_portNum_2, self.spinbox_portNum_3)
        MainWindow.setTabOrder(self.spinbox_portNum_3, self.btn_open)
        MainWindow.setTabOrder(self.btn_open, self.btn_close)
        MainWindow.setTabOrder(self.btn_close, self.btn_axis)
        MainWindow.setTabOrder(self.btn_axis, self.btn_zero)
        MainWindow.setTabOrder(self.btn_zero, self.btn_readPara)
        MainWindow.setTabOrder(self.btn_readPara, self.btn_savePara)
        MainWindow.setTabOrder(self.btn_savePara, self.btn_staticMeas)
        MainWindow.setTabOrder(self.btn_staticMeas, self.btn_dynaMeas)
        MainWindow.setTabOrder(self.btn_dynaMeas, self.checkbox_save)
        MainWindow.setTabOrder(self.checkbox_save, self.btn_laser_1)
        MainWindow.setTabOrder(self.btn_laser_1, self.btn_laser_2)
        MainWindow.setTabOrder(self.btn_laser_2, self.btn_laser_3)
        MainWindow.setTabOrder(self.btn_laser_3, self.tabWidget_2)
        MainWindow.setTabOrder(self.tabWidget_2, self.tabWidget_1)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "角度测量"))
        self.lab_dist.setText(_translate("MainWindow", "激光器读数：距离/mm"))
        self.btn_laser_1.setText(_translate("MainWindow", "关闭1号端口"))
        self.btn_laser_2.setText(_translate("MainWindow", "关闭2号端口"))
        self.btn_laser_3.setText(_translate("MainWindow", "关闭3号端口"))
        self.lab_staticMeas.setText(_translate("MainWindow", "静态测量结果：角度/°"))
        self.lab_dynaMeas.setText(_translate("MainWindow", "动态测量结果"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tabWidgetPage1), _translate("MainWindow", "结果"))
        self.connectBox.setTitle(_translate("MainWindow", "硬件连接"))
        self.spinbox_portNum_1.setPrefix(_translate("MainWindow", "COM"))
        self.btn_close.setText(_translate("MainWindow", "关闭设备"))
        self.lab_portNum_2.setText(_translate("MainWindow", "2号端口"))
        self.btn_open.setText(_translate("MainWindow", "连接设备"))
        self.lab_portNum_3.setText(_translate("MainWindow", "3号端口"))
        self.lab_portNum_1.setText(_translate("MainWindow", "1号端口"))
        self.spinbox_portNum_2.setPrefix(_translate("MainWindow", "COM"))
        self.spinbox_portNum_3.setPrefix(_translate("MainWindow", "COM"))
        self.openProgressBar.setFormat(_translate("MainWindow", "已打开%v/%m"))
        self.paraBox.setTitle(_translate("MainWindow", "参数确定"))
        self.btn_axis.setText(_translate("MainWindow", "旋转轴标定"))
        self.btn_zero.setText(_translate("MainWindow", "零位确定"))
        self.btn_readPara.setText(_translate("MainWindow", "读取参数"))
        self.btn_savePara.setText(_translate("MainWindow", "保存参数"))
        self.measureBox.setTitle(_translate("MainWindow", "角度测量"))
        self.btn_staticMeas.setText(_translate("MainWindow", "静态测量"))
        self.btn_dynaMeas.setText(_translate("MainWindow", "动态测量"))
        self.checkbox_save.setText(_translate("MainWindow", "保存至文件"))
        self.tabWidget_1.setTabText(self.tabWidget_1.indexOf(self.tab), _translate("MainWindow", "控制"))
from AngleMeasurement import ShowColor
from lineChartWgt import lineChartWgt
