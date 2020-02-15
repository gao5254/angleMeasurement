import pyMT3 as mt
import time
from PyQt5.QtCore import QThread, pyqtSignal, QMutex

class MyThread(QThread):

    # 设备打开成功信号
    openFinished = pyqtSignal(int)
    # 发生错误，错误代码
    errorOccured = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        # 定义线程锁
        self.threadLock = QMutex()
        # 定义待读取数据
        self.distance = 0.0
        # 定义扫描开关
        self.isScanning = False
        # 起始,读取时间
        self.beginTime = time.time()
        self.readingTime = time.time()
        # 通信句柄，index
        self.handle = 0.0
        self.ind = 0

    def run(self):
        while self.isScanning:
            (err, num, _) = mt.get_number(self.handle, self.ind)
            self.threadLock.lock()
            if err == 0:
                self.distance = num
            else:
                self.errorOccured.emit(err)
            self.threadLock.unlock()

    def my_open_device(self, portNum, openedNum):
        """
        打开设备
        :param portNum: 串口号（int）
        :param openedNum: 设备序号（int）
        :return: 是否打开（bool（0：成功；1：失败））
        """
        (err, self.handle, self.ind) = mt.open_device(portNum)
        if err == 0:
            self.openFinished.emit(openedNum)
            self.beginTime = time.time()
            return False
        else:
            self.errorOccured.emit(err)
            return True

    def my_start(self):
        """
        开始扫描
        :return: 线程开启（0：失败；1：成功）
        """
        self.isScanning = True
        self.start()
        return self.isRunning()

    def my_read(self):
        """
        获取当前线程激光位移传感器的读数和时间
        :return: 激光位移传感器读数和时间
        """
        self.threadLock.lock()
        self.readingTime = time.time()
        return self.distance, self.readingTime - self.beginTime

    def my_unlock(self):
        """
        关闭线程锁 
        """
        self.threadLock.unlock()

    def my_end(self):
        """
        关闭串口
        :return: 
        """
        self.isScanning = False
        mt.close_device(self.handle)

class hdwareConnector():
    def __init__(self):
        # 定义三个线程对象
        self.thread1 = MyThread()
        self.thread2 = MyThread()
        self.thread3 = MyThread()

    def open_devices(self, portNum):
        """
        接口函数，打开设备，并开始扫描
        :param portNum: 串口号（list）
        :return: 是否打开成功（bool（0：失败；1：成功））
        """
        # 开设备
        if self.thread1.my_open_device(portNum[0], 1) or\
            self.thread2.my_open_device(portNum[1], 2) or\
                self.thread3.my_open_device(portNum[2], 3):
            self.close_devices()
            return False

        # 开始扫描
        if self.thread1.my_start() and\
            self.thread2.my_start() and\
                self.thread3.my_start():
                return True
        else:
            self.close_devices()
            return False

    def get_distances(self):
        """
        接口函数，读取当前测量值和测量时间并返回
        :return: 测量时间测量值
        """
        distances = [0.0, 0.0, 0.0]
        readingTimes = [0.0, 0.0, 0.0]

        [distances[0], readingTimes[0]] = self.thread1.my_read()
        self.thread1.my_unlock()
        [distances[1], readingTimes[1]] = self.thread2.my_read()
        self.thread2.my_unlock()
        [distances[2], readingTimes[2]] = self.thread3.my_read()
        self.thread3.my_unlock()

        readingTime = sum(readingTimes) / 3
        returnValue = (readingTime, distances)

        return returnValue

    def close_devices(self):
        """
        接口函数，关闭设备，关闭线程
        :return: 关闭成功（bool（0：失败；1：成功））
        """
        self.thread1.my_end()
        self.thread2.my_end()
        self.thread3.my_end()
        self.thread1.terminate()
        self.thread2.terminate()
        self.thread3.terminate()
        if self.thread1.isFinished() and\
            self.thread2.isFinished() and\
                self.thread3.isFinished():
            return True
        else:
            return False



