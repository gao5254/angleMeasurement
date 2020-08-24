import numpy as np
from PyQt5.QtCore import QObject


class dataProcessor(QObject):
    def __init__(self):  # 构造函数
        self.cPara = {"Angle": None, "T": None}
        self.zeroDistance = np.ones(3)
        self.zeroVector = np.ones((1, 3))
        self.axis = np.ones(3)
        self.RArray = np.empty((9, ))

    def set_calib_para(self, calibPara):
        '''接口函数，设置标定参数
        供主程序调用，传入一个含有标定参数的字典，将其保存为类的内部成员变量，返回是否成功调用
        '''
        if 'Angle' in calibPara and 'T' in calibPara:
            self.cPara["Angle"] = np.array(calibPara["Angle"])
            self.cPara["T"] = np.array(calibPara["T"])
            self.RArray[0:3] = self.get_R_vector(self.cPara["Angle"][0:3])
            self.RArray[3:6] = self.get_R_vector(self.cPara["Angle"][3:6])
            self.RArray[6:9] = self.get_R_vector(self.cPara["Angle"][6:9])
            # print(self.RArray)
            return True
        else:
            return False

    def get_axis_para(self):
        '''接口函数，导出旋转轴参数和零位参数

        返回包含参数的字典
        '''
        axisPara = {
            'zeroDistance': self.zeroDistance.tolist(),
            'zeroVector': self.zeroVector.tolist(),
            'axis': self.axis.tolist()
        }
        return axisPara

    def get_R_vector(self, angles):
        alpha, beta, gamma = angles
        Rx = np.array([[1, 0, 0],
                       [0, np.cos(alpha), np.sin(alpha)],
                       [0, -np.sin(alpha), np.cos(alpha)]])
        Ry = np.array([[np.cos(beta), 0, -np.sin(beta)],
                       [0, 1, 0],
                       [np.sin(beta), 0, np.cos(beta)]])
        Rz = np.array([[np.cos(gamma), np.sin(gamma), 0],
                       [-np.sin(gamma), np.cos(gamma), 0],
                       [0, 0, 1]])
        R = np.dot(Rx, np.dot(Ry, Rz))
        return R[:, -1]

    def set_zero(self, distances: list) -> bool:
        '''接口函数，设置零位面

        供主程序调用，传入一个包含三个距离值的列表，计算零位面的位置并记录在类内部，返回是否成功设置
        '''
        self.zeroDistance = np.array(distances)
        self.zeroVector = self.get_vector(distances)
        return True

    def get_vector(self, distances):
        # 输入三个Z值，求取归一化法向量
        localZ = np.array(distances).reshape(-1, 3)
        point1 = np.dot(localZ[:, [0]], self.RArray[0:3].reshape(1, 3)) + self.cPara["T"][0:3].reshape(1, 3)
        point2 = np.dot(localZ[:, [1]], self.RArray[3:6].reshape(1, 3)) + self.cPara["T"][3:6].reshape(1, 3)
        point3 = np.dot(localZ[:, [2]], self.RArray[6:9].reshape(1, 3)) + self.cPara["T"][6:9].reshape(1, 3)

        # 三个点转化为两个向量
        vector1 = point2 - point1
        vector2 = point3 - point1

        normalvector = np.cross(vector1, vector2)
        sumall = np.linalg.norm(normalvector, axis=1, keepdims=True)
        newvector = normalvector / sumall

        # 返回归一化法向量
        return newvector

    def read_axis_raw(self, axisPara: dict) -> bool:
        '''接口函数，传入一个字典，读取旋转轴原始数据和零位数据，根据现有标定参数重新计算旋转轴参数和零位参数

        返回读取成功
        '''
        if 'zeroDistance' in axisPara and 'axisDistances' in axisPara:
            return self.set_axis_SVD(axisPara['axisDistances']) and self.set_zero(axisPara['zeroDistance'])
        else:
            return False

    def set_axis_SVD(self, distancesList: list) -> bool:
        '''接口函数，完成旋转轴标定过程
        供主程序调用，传入*二维列表*，进行旋转轴标定，并记录在类内部，返回是否成功设置
        '''
        # ncols = len(distancesList)
        # matrixA = np.ones((ncols, 3))
        # 求取SVD分解的矩阵A
        # for i in range(ncols):
        #     matrixA[i, :] = self.get_vector(distancesList[i]).ravel()
        matrixA = self.get_vector(distancesList)
        # 矩阵A减去均值
        matrixA = matrixA - np.mean(matrixA, 0)
        # SVD分解
        (_, _, vh) = np.linalg.svd(matrixA, full_matrices=False)
        # vh中最小的行向量即为旋转轴方向
        RotationAxis = vh[-1, :]
        # 旋转轴归一化
        # sumall = np.linalg.norm(RotationAxis)
        # RotationAxis = RotationAxis / sumall
        self.axis = np.squeeze(RotationAxis)
        return True

    def get_angle(self, distances):
        '''接口函数，完成角度计算
        供主程序调用，传入一个包含三个距离值的列表，根据标定参数、旋转轴、零位面计算旋转角度，返回计算得到的角度
        '''
        distances = np.array(distances).reshape(-1, 3)
        vector = self.get_vector(distances)
        NormalVector1 = np.cross(vector, self.axis)  # 向量叉乘
        NormalVector2 = np.cross(self.zeroVector, self.axis)  # 向量叉乘

        NormalVector1Length = np.linalg.norm(NormalVector1, axis=1)
        NormalVector2Length = np.linalg.norm(NormalVector2, axis=1)
        temp = np.sum(NormalVector1 * NormalVector2, axis=1)
        cos_angle = temp / (NormalVector1Length * NormalVector2Length)
        cos_angle[cos_angle > 1] = 1
        angle = np.arccos(cos_angle)
        angle = angle * 180 / np.pi

        # 判断distances第一个点正负
        angle[distances[:, 1] < self.zeroDistance[1]] = - angle[distances[:, 1] < self.zeroDistance[1]]
        return angle


# 实例
if __name__ == "__main__":
    import json
    processor = dataProcessor()
    with open('calibParaAngleT1.json', 'r') as fp:
        calibPara = json.load(fp)
    a = processor.set_calib_para(calibPara)

    with open('axisPara正.json', 'r') as fp:
        axisPara = json.load(fp)
    processor.read_axis_raw(axisPara)
    print(processor.axis)
    print("%" * 20)
    f = processor.get_angle([-5.497146606, 0.257499933, -14.20827293])
    print(f)
