from random import randint
def open_device(portNumber, deviceAddress = 0, baudRate = 57600):
    '''打开一个串口上的MT3激光位移计设备。

    返回其错误代码，串口句柄及设备编号。
    '''
    return (0, 0, 0)


def get_number(handle, deviceIndex):
    '''读取激光位移计设备读数

    返回错误代码，其读数，以及一个状态量
    '''
    return (0, randint(100, 200), 0)

def close_device(handle):
    '''关闭串口及其关联设备

    返回错误代码
    '''
    return 0