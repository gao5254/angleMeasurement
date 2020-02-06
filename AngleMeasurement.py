# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 22:09:45 2020

@author: kami
"""
from ui import Ui_MainWindow
import dataPrpcessor                    
import hdwareConnector 
import axisDlg
import lineChartWgt
import csvwriter

import sys
import json
from PyQt5 import QtWidgets    
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer

class MyMainWindow(QtWidgets.QMainWindow,Ui_MainWindow):  
    def __init__(self,parent=None): 
        super(MyMainWindow,self).__init__(parent)        
        self.setupUi(self)                                 
        self.timestatus = 3000 
        
        # 重写成员变量
        self.hdweConnector = hdwareConnector.hdwareConnector()
        self.dataProcessor = dataPrpcessor.dataPrpcessor()
        self.axisCalib = axisDlg.axisDlg()
        # self.dynaChart = lineChartWgt.lineChartWgt()  
        self.datasaver = csvwriter.csvWriter() 
        
        # 信号
        self.hdweConnector.openFinished.connect(self.Signal_portFin)
        self.hdweConnector.errorOccured.connect(self.Signal_hdweError)
        
        # 按钮
        self.btn_open.clicked.connect(self.Open_Devices)
        self.btn_close.clicked.connect(self.Close_Devices)
        self.btn_axis.clicked.connect(self.Set_Axis)
        self.btn_zero.clicked.connect(self.Set_Zero)
        self.btn_staticMeas.clicked.connect(self.Meas_Static)
        self.btn_dynaMeas.toggled.connect(self.Meas_Dynamic)
        
        # 定时器
        self.timer_showDist = QTimer(self)
        self.timer_showDist.timeout.connect(self.show_dist)
        self.timer_showDist.start(2000)
        
        # 标定激光器参数
        with open("calibPara.json",'r') as load_f:
            load_dict = json.load(load_f)
        if set_calib_para(load_dict):
           self.statusBar().showMessage('成功标定激光器参数',self.timestatus)
        else: self.statusBar().showMessage('错误：请检查标定参数文件',self.timestatus)
        
        
    # 信号处理函数
    def Signal_portFin(self,number):
        '''
        依次显示已成功连接的端口号；处理openFinished信号
        ''' 
        self.statusBar().showMessage(str(number) + '号端口已成功连接',self.timestatus)
        
    def Signal_hdweError(self,code):    
        '''
        显示硬件错误代码；处理errorOccured信号
        '''         
        self.statusBar().showMessage('硬件错误代码：'+str(code) + '，请检查硬件连接',self.timestatus)
        self.btn_axis.setEnabled(False)
        self.btn_zero.setEnabled(False)
        self.btn_staticMeas.setEnabled(False)
        self.btn_dynaMeas.setEnabled(False)
        self.btn_save.setEnabled(False)
        self.timer_showDist.stop() 
        # *关掉timer（实时显示+动态测量）

    # 功能函数
    def Open_Devices(self): 
        '''
        连接硬件设备，标定激光器参数
        ''' 
        # 读取端口号
        portnumber = [ self.PortNumber.value(),
                       self.PortNumber.value() + 1, 
                       self.PortNumber.value() + 2 ]
        # 打开设备并开启线程进行扫描
        if self.hdweConnector.open_devices(portnumber):
            self.statusBar().showMessage('成功连接端口',self.timestatus)
            self.btn_close.setEnabled(True) 
            self.btn_axis.setEnabled(True) 
        else: self.statusBar().showMessage('错误：无法连接端口，请检查端口重试',self.timestatus)
    
    def show_dist():
        '''
        实时显示激光位移器距离读数
        '''          
        [time,distances] = self.hdweConnector.get_distances()
        self.lcdnum_dist1.display(distances[0])
        self.lcdnum_dist2.display(distances[1])
        self.lcdnum_dist3.display(distances[2])        
   
    def Set_Axis(self):
        '''
        旋转轴标定  
        '''
        self.axisCalib.show()
        self.axisCalib.distancesNeeded.connect(self.Get_Axis)
        self.axisCalib.gatherFinished.connect(self.Calc_Axis)
    
    def Get_Axis(self):
        '''
        旋转轴标定：获取数据  
        '''       
        print("distancesNeeded")
        [time,distances] = self.hdweConnector.get_distances()
        self.axisCalib.set_distances(distances)

    def Calc_Axis(self,twoDimenList):
        '''
        旋转轴标定：计算过程  
        '''        
        print("gatherFinished")
        if self.dataProcessor.set_axis(twoDimenList):
            self.statusBar().showMessage('成功标定旋转轴',self.timestatus)
            self.btn_zero.setEnabled(True)
        else: self.statusBar().showMessage('错误：标定旋转轴失败',self.timestatus)        

    def Set_Zero(self):
        '''
        零位确定
        '''
        [time,distances] = self.hdweConnector.get_distances()
        if self.dataProcessor.set_zero(distances):
            self.statusBar().showMessage('成功确定零位面',self.timestatus)
            self.btn_staticMeas.setEnabled(True)
            self.btn_dynaMeas.setEnabled(True)
            self.btn_save.setEnabled(True)
        else: self.statusBar().showMessage('错误：确定零位面失败',self.timestatus)

    def Meas_Static(self):
        '''
        静态测量
        '''            
        [time,distances] = self.hdweConnector.get_distances()
        self.lcdnum_staticMeas.display(self.dataProcessor.get_angle(distances))

    def Meas_Dynamic(self,isChecked):
        '''
        动态测量：状态判断
        '''
        if isChecked == True:
            # 按下状态，开启定时器
            self.btn_dynaMeas.setText('关闭动态测量') 
            self.timer_measdyna = QTimer(self)
            self.timer_measdyna.timeout.connect(self.MeasDynamic)
            self.timer_measdyna.start(2000) 
        else:
            # 弹起状态，关闭定时器
            self.btn_dynaMeas.setText('动态测量')
            self.timer_measdyna.stop()

    def MeasDynamic():       
        '''
        动态测量：计算及绘图
        ''' 

                
    def Close_Devices(self):
        '''
        关闭设备
        ''' 
        reply = QMessageBox.question(self, 'Message','确定关闭设备吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes: 
            self.hdweConnector.close_devices()

            
    def closeEvent(self, event):
        '''
        关闭对话框
        ''' 
        reply = QMessageBox.question(self, 'Message', '确定退出程序吗?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()    



if __name__ == '__main__':       
    app = QApplication(sys.argv) 
    MMW = MyMainWindow()         
    MMW.show()                   
    sys.exit(app.exec_())        
    # hhhhhhhhhhhh

            
