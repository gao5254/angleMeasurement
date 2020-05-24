import time

from PyQt5.QtCore import QMutex, QObject, QThread, pyqtSignal
from typing import List
import pyMT3 as mt

# import fakeMT as mt
# from random import randint


class MyThread(QThread):

    # 发生错误，错误出现地方，错误代码
    errorHappened = pyqtSignal(str, int)

    def __init__(self):
        super().__init__()

        # 定义线程锁
        self.disLock = QMutex()
        self.comLock = QMutex()
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
            self.comLock.lock()
            (err, num, _) = mt.get_number(self.handle, self.ind)
            self.comLock.unlock()
            if err == 0:
                self.disLock.lock()
                self.distance = num
                self.readingTime = time.time()
                self.disLock.unlock()
            else:
                self.errorHappened.emit('获取读数', err)
                break

    def my_open_device(self, portNum, openedNum):
        """
        打开设备
        :param portNum: 串口号（int）
        :param openedNum: 设备序号（int）
        :return: 是否打开（bool（1：成功；0：失败））
        """
        self.comLock.lock()
        (err, self.handle, self.ind) = mt.open_device(portNum)
        self.comLock.unlock()
        if err == 0:
            # self.openFinished.emit(openedNum)
            # self.beginTime = time.time()
            self.isConnecting = True
            return True
        else:
            self.isConnecting = False
            self.errorHappened.emit('打开设备', err)
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
        self.disLock.lock()
        num = self.distance
        readTime = self.readingTime
        self.disLock.unlock()
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
            self.comLock.lock()
            mt.close_device(self.handle)
            self.comLock.unlock()
            self.isConnecting = False

    def my_turn_onoff(self, onOff):
        if self.isConnecting:
            self.comLock.lock()
            err = mt.turnonoff_device(self.handle, self.ind, onOff)
            self.comLock.unlock()
            if err != 0:
                self.errorHappened.emit('开关激光光点', err)
                return False
            else:
                return True
        else:
            return False

    def my_set_fre(self, fre):
        if self.isConnecting and fre in mt.filterFrequencyList:
            self.comLock.lock()
            err = mt.set_filter_index(self.handle, self.ind, mt.filterFrequencyList.index(fre))
            self.comLock.unlock()
            if err != 0:
                self.errorHappened.emit('设置滤波频率', err)
                return False
            else:
                return True
        else:
            return False

    def my_get_fre(self):
        if self.isConnecting:
            self.comLock.lock()
            (err, fre) = mt.get_filter_frequency(self.handle, self.ind)
            self.comLock.unlock()
            return fre


class hdwareConnector(QObject):

    # 设备打开成功信号
    openFinished = pyqtSignal(int)
    # 发生错误，错误代码
    errorOccured = pyqtSignal(str)

    def __init__(self):
        super(hdwareConnector, self).__init__()
        # 定义三个线程对象
        # self.threads = [MyThread(), MyThread(), MyThread()]
        self.threads: List[MyThread] = [MyThread(), MyThread(), MyThread()]
        # 信号连接
        # for i in range(3):
        #     self.threads[i].errorHappened.connect(lambda loc, err: self.OnErrorHappened(i, loc, err))
        self.threads[0].errorHappened.connect(lambda loc, err: self.OnErrorHappened(0, loc, err))
        self.threads[1].errorHappened.connect(lambda loc, err: self.OnErrorHappened(1, loc, err))
        self.threads[2].errorHappened.connect(lambda loc, err: self.OnErrorHappened(2, loc, err))
        
    def OnErrorHappened(self, ind, loc, err):
        errStr = str(ind + 1) + '号端口的(' + loc + ')过程\n' + str(err) + ':' + mt.get_error_text(err)
        self.errorOccured.emit(errStr)

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
            # print(self.threads[i].my_get_fre())
            if not self.threads[i].my_set_fre(200):
                return False
            # print(self.threads[i].my_get_fre())
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
        # 测试用例
        # return [time.time(),[randint(80, 120),randint(80, 120),randint(80, 120)]]

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

    def turnonoff_laser(self, ind, onOff):
        '''接口函数，打开或关闭某个激光器光点

        ind标识激光器编号（0，1，2），onOff标识打开或关闭（false关闭，true打开）
        返回是否成功
        '''
        return self.threads[ind].my_turn_onoff(int(onOff))


if __name__ == "__main__":
    myConnector = hdwareConnector()
    myConnector.open_devices([3, 4, 5])
    thistime = time.time()
    # for i in range(5):
    #     time.sleep(0.5)
    #     res = myConnector.get_distances()
    #     print(res)
    # print('\n\n')
    # time.sleep(1)
    # myConnector.turnonoff_laser(0, False)
    # time.sleep(2)
    # for i in range(10):
    #     time.sleep(0.1)
    #     res = myConnector.get_distances()
    #     print(res)
    # print('\n\n')
    # print(myConnector.threads[0].isRunning())
    # print(myConnector.turnonoff_laser(0, True))
    # time.sleep(1)
    for i in range(20):
        time.sleep(0.05)
        res = myConnector.get_distances()
        print(res)

    thattime = time.time()
    print(thattime - thistime)
    myConnector.close_devices()
