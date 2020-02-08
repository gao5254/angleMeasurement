# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 22:09:45 2020

@author: kami

"""

"""
测试用例
"""
from random import randint
import time
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget


class hdwareConnector(QObject):
    # 完成打开设备的信号，每打开一个设备发送一次，返回已经打开的设备个数
    # def __init__(self, *args, **kwargs):
    def __init__(self):
        # 定义三个线程对象
        # self.threads = [thread1, thread2, thread3]
        super().__init__() 
        
    openFinished = QtCore.pyqtSignal(int)
    errorOccured = QtCore.pyqtSignal(int)

    def open_devices(self, portNum) -> bool:
        '''接口函数，完成打开设备并开启线程进行扫描

        供主程序调用，传入串口号列表，在内部开启三个线程，打开设备，并循环扫描，返回是否成功打开三个设备
        '''
        if isinstance(portNum,list):
            self.openFinished.emit(3)
            return True


    def get_distances(self):
        '''接口函数，读取测头数据并返回

        供主程序调用，读取三个侧头的读数，记录当前时间，并返回一个元组
        '''
        return [time.time(),[randint(80, 120),randint(80, 120),randint(80, 120)]]

    def close_devices(self):
        '''接口函数，关闭设备，关闭线程

        供主程序调用，返回是否关闭成功
        '''
        print('Closing...')
        return True

# self.hdweConnector.openFinished.connect(self.Signal_portFin)，错误提示：
# 1.cannot be converted to PyQt5.QtCore.QObject in this context
# 原因：hdwareConnector不是PyQt5里面的类，也没有继承PyQt5里面的类，所以不能用信号
# 解决方案：hdwareConnector继承QObject，然后就可以发信号
# 2.RuntimeError: super-class __init__() of type TCPConnect was never called
# 原因：没有使用__init__()和super()进行初始化
# 解决方法：添加def __init__(self):
#                   super().__init__()
# 3.AttributeError: 'PyQt5.QtCore.pyqtSignal' object has no attribute 'connect'
# 原因：pyqt5信号要定义为类属性，而不是放在_init_()方法里面
# 解决方法：把openFinished = QtCore.pyqtSignal(int)从_init_()里拿出来