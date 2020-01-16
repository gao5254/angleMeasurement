# 发哥的算法类
class dataPrpcessor(object):
    def __init__(self):
        # 标定参数的具体形式
        self.cPara = {
            "parallelRatio":[1, 1, 1]
            "frontOffset":[1, 1, 1]
            "xyCoordinate":[[1, 1], [1, 1], [1, 1]]
        }

    def set_calib_para(self, calibPara : dict): -> bool
        '''接口函数，设置标定参数

        供主程序调用，传入一个含有标定参数的字典，将其保存为类的内部成员变量，返回是否成功调用
        '''
        pass
    
    def get_corrected_distances(self, distances : list): -> list
        '''接口函数，计算校正后的距离值

        供主程序调用，传入原始距离值，返回校正后距离值
        '''
        pass


    def set_zero(self, distances : list): -> bool
        '''接口函数，设置零位面

        供主程序调用，传入一个包含三个距离值的列表，计算零位面的位置并记录在类内部，返回是否成功设置
        '''
        pass

    def set_axis(self, distancesList : list): -> bool
        '''接口函数，完成旋转轴标定过程

        供主程序调用，传入*二维列表*，进行旋转轴标定，并记录在类内部，返回是否成功设置
        '''
        pass

    def get_angle(self, distances : list): -> float
        '''接口函数，完成角度计算

        供主程序调用，传入一个包含三个距离值的列表，根据标定参数、旋转轴、零位面计算旋转角度，返回计算得到的角度
        '''
        pass

# 发哥的硬件通信类
class hdwareConnector(object):

    # 完成打开设备的信号，每打开一个设备发送一次，返回已经打开的设备个数
    openFinished = pyqtSignal(int)


    def __init__(self):
        # 定义三个线程对象
        self.threads = [thread1, thread2, thread3]

    def open_devices(self, portNum : list): -> bool
        '''接口函数，完成打开设备并开启线程进行扫描

        供主程序调用，传入串口号列表，在内部开启三个线程，打开设备，并循环扫描，返回是否成功打开三个设备
        '''
        pass

    def get_distances(self): -> （int, list)
        '''接口函数，读取测头数据并返回

        供主程序调用，读取三个侧头的读数，记录当前时间，并返回一个元组
        '''
        pass

    def close_devices(self): -> bool
        '''接口函数，关闭设备，关闭线程

        供主程序调用，返回是否关闭成功
        '''
        pass

# 鲍大神的旋转轴标定对话框

class axisDlg(object):

    # 需要外界传入距离的信号
    distancesNeeded = pyqtSignal()

    # 数据采集完成的信号,传出采集到的距离的*二维列表*
    gatherFinished = pyqtSignal(list)

    def set_distances(self, distances : list): ->bool
        '''接口函数，接受距离列表

        供主程序调用，传入距离列表，显示并记录在类内部，返回设置成功
        '''
        pass

# 鲍大神的绘图类
class lineChartWgt(object):

    def add_angle(self, curTime : int, curAngle : float): ->bool
        '''接口函数，接收一个新角度，并进行绘图

        供主程序调用，传入时间和角度，进行绘图，返回接收成功
        '''
        pass