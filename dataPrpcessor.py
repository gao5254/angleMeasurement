# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 22:09:45 2020

@author: kami

"""

"""
测试用例
"""
from random import randint

class dataPrpcessor(object):
    def set_calib_para(self, calibPara):
        '''接口函数，设置标定参数

        供主程序调用，传入一个含有标定参数的字典，将其保存为类的内部成员变量，返回是否成功调用
        '''
        if isinstance(calibPara, dict):
            return True
    # def get_corrected_distances(self, distances: list) -> list:
    #     '''接口函数，计算校正后的距离值

    #     供主程序调用，传入原始距离值，返回校正后距离值
    #     '''
    #     pass


    def set_zero(self, distances):
        '''接口函数，设置零位面

        供主程序调用，传入一个包含三个距离值的列表，计算零位面的位置并记录在类内部，返回是否成功设置
        '''
        if isinstance(distances, list):
            return True

    def set_axis(self, distancesList):
        '''接口函数，完成旋转轴标定过程

        供主程序调用，传入*二维列表*，进行旋转轴标定，并记录在类内部，返回是否成功设置
        '''
        if isinstance(distancesList, list):
            return True

    def get_angle(self, distances):
        '''接口函数，完成角度计算

        供主程序调用，传入一个包含三个距离值的列表，根据标定参数、旋转轴、零位面计算旋转角度，返回计算得到的角度
        '''
        if isinstance(distances, list):
            return randint(80, 120)

if __name__ == '__main__':
    print('dataPrpcessor')