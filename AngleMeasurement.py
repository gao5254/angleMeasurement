# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 22:09:45 2020

@author: kami
"""
from ui import Ui_MainWindow
import dataProcessor                    
import HDwareConnector 
import asixDlg
import csvwriter

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer
import sys
import json
import time    

class MyMainWindow(QMainWindow,Ui_MainWindow):  
    def __init__(self,parent=None): 
        super(MyMainWindow,self).__init__(parent)        
        self.setupUi(self)                               
        self.timestatus = 3000 

        # 重写成员变量
        self.hdweConnector = HDwareConnector.hdwareConnector()
        self.dataProcessor = dataProcessor.dataProcessor()
        self.axisCalib = asixDlg.axisDlg()
        self.datasaver = csvwriter.csvWriter(self) 
        
        # 信号
        self.hdweConnector.openFinished.connect(self.Signal_portFin)
        self.hdweConnector.errorOccured.connect(self.Signal_hdweError)
        self.axisCalib.distancesNeeded.connect(self.Get_Axis)
        self.axisCalib.gatherFinished.connect(self.Calc_Axis)
        
        # 按钮
        self.btn_open.clicked.connect(self.Open_Devices)
        self.btn_close.clicked.connect(self.Close_Devices)
        self.btn_axis.clicked.connect(self.Set_Axis)
        self.btn_zero.clicked.connect(self.Set_Zero)
        self.btn_staticMeas.clicked.connect(self.Meas_Static)
        self.btn_dynaMeas.toggled.connect(self.Meas_Dynamic)
        
        # 定时器
        self.timer_showDist = QTimer(self)
        self.timer_showDist.timeout.connect(self.Show_Dist)
        self.timer_measdyna = QTimer(self)
        self.timer_measdyna.timeout.connect(self.MeasDynamic)
        
        # 标定激光器参数
        # 测试用例
        testDict = {"parallelRatio":[1, 1, 1],
                    "frontOffset":[1, 1, 1],
                    "xyCoordinate":[[0, 0], [0, 1], [1, 0]]}
        testJson = json.dumps(testDict)
        with open("..\\calibPara.json",'w') as write_f:
            write_f.write(testJson)
            write_f.close()

        with open("..\\calibPara.json",'r') as load_f:
            load_dict = json.load(load_f)
        if self.dataProcessor.set_calib_para(load_dict): 
            self.btn_open.setEnabled(True)
            self.statusBar().showMessage('成功标定激光器参数',self.timestatus)
        else: QMessageBox.critical(self, '错误提示','激光器标定失败')
        
        
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
        self.Close_Devices()
        QMessageBox.critical(self, '错误提示','硬件连接错误，错误代码'+str(code))

    # 功能函数
    def Open_Devices(self): 
        '''
        连接硬件设备，标定激光器参数
        ''' 
        # 读取端口号
        portnumber = [ self.spinbox_portNum.value(),
                       self.spinbox_portNum.value() + 1, 
                       self.spinbox_portNum.value() + 2 ]
        # 打开设备并开启线程进行扫描
        if self.hdweConnector.open_devices(portnumber):
            self.statusBar().showMessage('成功连接设备',self.timestatus)
            self.btn_close.setEnabled(True) 
            self.btn_axis.setEnabled(True) 
            self.timer_showDist.start(2000)
        else: QMessageBox.critical(self, '错误提示','硬件连接失败')
    
    def Show_Dist(self):
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
        else: QMessageBox.critical(self, '错误提示','标定旋转轴失败')        

    def Set_Zero(self):
        '''
        零位确定
        '''
        [time,distances] = self.hdweConnector.get_distances()
        if self.dataProcessor.set_zero(distances):
            self.statusBar().showMessage('成功确定零位面',self.timestatus)
            self.btn_staticMeas.setEnabled(True)
            self.btn_dynaMeas.setEnabled(True)
            self.checkbox_save.setEnabled(True)
        else: QMessageBox.critical(self, '错误提示','确定零位面失败')

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
            if self.checkbox_save.isChecked():
                self.datasaver.start_writing()
            self.lineChartWgt.clearSeries()
            self.btn_staticMeas.setEnabled(False)
            self.btn_dynaMeas.setText('关闭动态测量') 
            self.checkbox_save.setEnabled(False)
            self.t_start = time.time()
            self.timer_measdyna.start(100) 
        else:
            # 弹起状态，关闭定时器
            self.btn_dynaMeas.setText('动态测量')
            self.btn_staticMeas.setEnabled(True)
            self.checkbox_save.setEnabled(True)
            self.timer_measdyna.stop()
            if self.checkbox_save.isChecked():
                self.datasaver.stop_writing()   

    def MeasDynamic(self):       
        '''
        动态测量：计算及绘图
        ''' 
        self.statusBar().showMessage('正在动态测量',self.timestatus)
        [time,distances] = self.hdweConnector.get_distances()
        angle = self.dataProcessor.get_angle(distances) 
        self.lcdnum_staticMeas.display(angle)
        self.lineChartWgt.add_angle(time-self.t_start,angle)               
        if self.checkbox_save.isChecked(): 
            if self.datasaver.write_distances(time-self.t_start,distances,angle):
                print('Saving...')               
                
    def Close_Devices(self):
        '''
        关闭设备
        ''' 
        # reply = QMessageBox.question(self, 'Message','确定关闭设备吗?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # if reply == QMessageBox.Yes: 
        self.timer_showDist.stop() 
        self.btn_dynaMeas.setChecked(False)    # 触发Meas_Dynamic中的弹起部分
        self.btn_axis.setEnabled(False)
        self.btn_zero.setEnabled(False)
        self.btn_staticMeas.setEnabled(False)
        self.btn_dynaMeas.setEnabled(False)
        self.checkbox_save.setEnabled(False)
        self.hdweConnector.close_devices()
         
    def closeEvent(self, event):
        '''
        关闭对话框
        ''' 
        reply = QMessageBox.question(self, 'Message', '确定退出程序吗?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.Close_Devices()
            event.accept()
        else:
            event.ignore()    


if __name__ == '__main__':       
    app = QApplication(sys.argv) 
    MMW = MyMainWindow()         
    MMW.show()                   
    sys.exit(app.exec_())        