import pyMT3 as mt
# import fakeMT as mt
import time
from PyQt5.QtCore import QThread, pyqtSignal, QMutex, QObject

class MyThread(QThread):

    # 发生错误，错误代码
    errorHappened = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        # 定义线程锁
        self.threadLock = QMutex()
        # 定义待读取数据
        self.distance = 0.0
        # 定义扫描开关
        self.isScanning = False
        # 起始,读取时间
        # self.beginTime = time.time()
        self.readingTime = time.time()
        # 通信句柄，index
        self.handle = 0.0
        self.ind = 0
        # 设备连接状态
        self.isConnecting = False

    def run(self):
        while self.isScanning:
            (err, num, _) = mt.get_number(self.handle, self.ind)
            if err == 0:
                self.threadLock.lock()
                self.distance = num
                self.readingTime = time.time()
                self.threadLock.unlock()
            else:
                self.errorHappened.emit(err)
                break

    def my_open_device(self, portNum, openedNum):
        """
        打开设备
        :param portNum: 串口号（int）
        :param openedNum: 设备序号（int）
        :return: 是否打开（bool（1：成功；0：失败））
        """
        (err, self.handle, self.ind) = mt.open_device(portNum)
        if err == 0:
            # self.openFinished.emit(openedNum)
            # self.beginTime = time.time()
            self.isConnecting = True
            return True
        else:
            self.isConnecting = False
            # self.errorHappened.emit(err)
            return False

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
        num = self.distance
        readTime = self.readingTime
        self.threadLock.unlock()
        return (num, readTime)

    # def my_unlock(self):
    #     """
    #     关闭线程锁 
    #     """
    #     self.threadLock.unlock()

    def my_end(self):
        """
        关闭串口
        :return: 
        """
        self.isScanning = False
        # mt.close_device(self.handle)

    def my_close(self):
        """
        关闭设备，返回true/false
        """
        if self.isConnecting:
            mt.close_device(self.handle)
            self.isConnecting = False

class hdwareConnector(QObject):

    # 设备打开成功信号
    openFinished = pyqtSignal(int)
    # 发生错误，错误代码
    errorOccured = pyqtSignal(int)


    def __init__(self):
        super(hdwareConnector, self).__init__()
        # 定义三个线程对象
        self.threads = [MyThread(), MyThread(), MyThread()]
        # 信号连接
        for i in range(3):
            self.threads[i].errorHappened.connect(self.OnErrorHappened)

    def OnErrorHappened(self, err):
        self.errorOccured.emit(err)

    def open_devices(self, portNum):
        """
        接口函数，打开设备，并开始扫描
        :param portNum: 串口号（list）
        :return: 是否打开成功（bool（0：失败；1：成功））
        """
        # # 开设备
        # if self.thread1.my_open_device(portNum[0], 1) or\
        #     self.thread2.my_open_device(portNum[1], 2) or\
        #         self.thread3.my_open_device(portNum[2], 3):
        #     self.close_devices()
        #     return False

        # # 开始扫描
        # if self.thread1.my_start() and\
        #     self.thread2.my_start() and\
        #         self.thread3.my_start():
        #         return True
        # else:
        #     self.close_devices()
        #     return False
        for i in range(3):
            if not self.threads[i].my_open_device(portNum[i], i):
                return False
        for i in range(3):
            if not self.threads[i].my_start():
                self.close_devices()
                return False
            self.openFinished.emit(i+1)
        return True
            

    def get_distances(self):
        """
        接口函数，读取当前测量值和测量时间并返回
        :return: 测量时间测量值
        """
        distances = [0.0, 0.0, 0.0]
        readingTimes = [0.0, 0.0, 0.0]

        for i in range(3):
            (distances[i], readingTimes[i]) = self.threads[i].my_read()

        # 取三个读取时间的均值作为实际时间
        readingTime = sum(readingTimes) / 3
        returnValue = (readingTime, distances)

        return returnValue

    def close_devices(self):
        """
        接口函数，关闭设备，关闭线程
        :return: 关闭成功（bool（0：失败；1：成功））
        """
        for i in range(3):
            self.threads[i].my_end()
            self.threads[i].wait()
            self.threads[i].my_close()

        return True


if __name__ == "__main__":
    myConnector = hdwareConnector()
    myConnector.open_devices([4,5,6])
    thistime = time.time()
    for i in range(100):
        res =myConnector.get_distances()
        # print(res)
    thattime = time.time()
    print(thattime - thistime)
    myConnector.close_devices()

