import numpy as np
from PyQt5.QtCore import QObject


class dataProcessor(QObject):
    def __init__(self):  # 构造函数
        self.cPara = {
            "parallelRatio": [1, 1, 1],
            "frontOffset": [1, 1, 1],
            "xyCoordinate": [[1, 1], [1, 1], [1, 1]]
        }
        self.zeroDistance = np.ones(3)
        self.zeroVector = np.ones(3)
        self.axis = np.ones(3)
        self.RotationMatrix = np.array(
            [[1 / (3**0.5), -1 / (3**0.5), -1 / (3**0.5)],
             [1 / (6**0.5), 2**0.5 / 3**0.5, -1 / (6**0.5)],
             [1 / (2**0.5), 0, 1 / (2**0.5)]])
        # self.RotationMatrix = np.array([[1/2, -1/(2**0.5), -1/2], [1/2, 1/2**0.5, 1/2], [-1/(2**0.5), 0, 1/(2**0.5)]])

    def set_calib_para(self, calibPara):
        '''接口函数，设置标定参数
        供主程序调用，传入一个含有标定参数的字典，将其保存为类的内部成员变量，返回是否成功调用
        '''
        if 'parallelRatio' in calibPara and 'frontOffset' in calibPara and 'xyCoordinate' in calibPara:
            self.cPara['parallelRatio'] = calibPara['parallelRatio']
            self.cPara['frontOffset'] = calibPara['frontOffset']
            self.cPara['xyCoordinate'] = calibPara['xyCoordinate']
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

    def get_corrected_distances(self, distances: list) -> list:
        '''接口函数，计算校正后的距离值
        供主程序调用，传入原始距离值，返回校正后距离值
        '''
        # NewDistances = [k*x + b for x, k, b in zip(distances, self.cPara['parallelRatio'], self.cPara['frontOffset'])]
        # NewDistances[0] = distances[0] * self.cPara['parallelRatio'][
        #     0] + self.cPara['frontOffset'][0]
        # NewDistances[1] = distances[1] * self.cPara['parallelRatio'][
        #     1] + self.cPara['frontOffset'][1]
        # NewDistances[2] = distances[2] * self.cPara['parallelRatio'][
        #     2] + self.cPara['frontOffset'][2]
        
        # 矩阵兼容性
        NewDistances = distances * self.cPara['parallelRatio'] + self.cPara['frontOffset']
        return NewDistances

    def set_zero(self, distances: list) -> bool:
        '''接口函数，设置零位面

        供主程序调用，传入一个包含三个距离值的列表，计算零位面的位置并记录在类内部，返回是否成功设置
        '''
        self.zeroDistance = np.array(distances)
        self.zeroVector = self.get_vector(distances)
        return True

    def get_vector(self, distances: list):
        # 输入三个Z值，求取归一化法向量
        distances = np.array(distances).reshape(-1, 3)
        RightDistances = self.get_corrected_distances(distances)
        shape = RightDistances.shape
        point1 = np.empty((shape[0], 3))
        point1[:, 0] = self.cPara['xyCoordinate'][0, 0]
        point1[:, 1] = self.cPara['xyCoordinate'][0, 1]
        point1[:, 2] = RightDistances[:, 0]

        point2 = np.empty((shape[0], 3))
        point2[:, 0] = self.cPara['xyCoordinate'][1, 0]
        point2[:, 1] = self.cPara['xyCoordinate'][1, 1]
        point2[:, 2] = RightDistances[:, 1]

        point3 = np.empty((shape[0], 3))
        point3[:, 0] = self.cPara['xyCoordinate'][2, 0]
        point3[:, 1] = self.cPara['xyCoordinate'][2, 1]
        point3[:, 2] = RightDistances[:, 2]

        # 三个点转化为两个向量
        vector1 = point2 - point1
        vector2 = point3 - point1
        # vector1 = [
        #     point2[0] - point1[0], point2[1] - point1[1], point2[2] - point1[2]
        # ]
        # vector2 = [
        #     point3[0] - point1[0], point3[1] - point1[1], point3[2] - point1[2]
        # ]

        # 添加旋转矩阵
        # vector1 = np.dot(self.RotationMatrix, vector1)
        # vector2 = np.dot(self.RotationMatrix, vector2)

        # 两个向量求法向量，并归一化
        # normalvector = [1, 1, 1]
        # newvector = [1, 1, 1]
        # normalvector[0] = vector1[1] * vector2[2] - vector2[1] * vector1[2]
        # normalvector[1] = vector1[0] * vector2[2] - vector2[0] * vector1[2]
        # normalvector[2] = vector1[0] * vector2[1] - vector2[0] * vector1[1]
        normalvector = np.cross(vector1, vector2)
        sumall = np.linalg.norm(normalvector)
        newvector = normalvector / sumall

        # 返回归一化法向量
        return newvector

    def read_axis(self, axisPara: dict) -> bool:
        '''接口函数，传入一个字典，直接读取其中旋转轴参数和零位参数

        返回读取成功
        '''
        if 'zeroDistance' in axisPara and 'zeroVector' in axisPara and 'axis' in axisPara:
            self.zeroDistance = np.array(axisPara['zeroDistance'])
            self.zeroVector = np.array(axisPara['zeroVector'])
            self.axis = np.array(axisPara['axis'])
            return True
        else:
            return False

    def read_axis_raw(self, axisPara: dict) -> bool:
        '''接口函数，传入一个字典，读取旋转轴原始数据和零位数据，根据现有标定参数重新计算旋转轴参数和零位参数

        返回读取成功
        '''
        if 'zeroDistance' in axisPara and 'axisDistances' in axisPara:
            return self.set_axis_SVD(axisPara['axisDistances']) and self.set_zero(axisPara['zeroDistance'])
        else:
            return False

    def set_axis(self, distancesList: list) -> bool:
        '''接口函数，完成旋转轴标定过程
        供主程序调用，传入*二维列表*，进行旋转轴标定，并记录在类内部，返回是否成功设置
        '''
        ncols = len(distancesList)
        matrixA = np.ones((ncols, 3))
        # 求取最小二乘法G矩阵
        for i in range(ncols):
            # array[i]=self.get_corrected_distances(distancesList[i])
            matrixA[i, :] = self.get_vector(distancesList[i])
        # 将列表转化为矩阵
        NewArray = np.ones((ncols, 1))
        # NewMatrix = np.array(NewArray)
        # NewMatrixA = np.array(array)
        # NewMatrixA = np.transpose(NewMatrixA)
        # NewMatrixA = np.dot(self.RotationMatrix, NewMatrixA)
        # NewMatrixA = np.transpose(NewMatrixA)  # n*3
        # NewMatrixAt = np.transpose(NewMatrixA)  # 转置
        # 最小二乘法求旋转轴
        RotationAxis = np.linalg.lstsq(matrixA, NewArray, rcond=None)[0]
        # 旋转轴乘以旋转矩阵，并归一化
        sumall = np.linalg.norm(RotationAxis)
        self.axis = RotationAxis / sumall
        self.axis = np.squeeze(self.axis)
        return True

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

    def get_angle(self, distances: list) -> float:
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
    processor1 = dataProcessor()
    with open('calibPara.json', 'r') as fp:
        calibPara = json.load(fp)
    a = processor1.set_calib_para(calibPara)
    # print(a)
    # b = processor1.get_corrected_distances([1, 1, 1])
    # print(b)
    # c = processor1.get_vector([4, 8, 10])
    # print(c)
    # d = processor1.set_zero([0.303, -0.3955, 0.3187])
    # print(d)
    # e = processor1.set_axis([[0.30385, -0.395596, 0.318728], [1.07997,10.8051,-9.68715], [1.53737,22.3281,-20.6895],
    #                          [-0.656339	,-11.8904,10.1878], [-2.25074,-24.3517,20.4447]])
    # print(processor1.axis)
    with open('axisPara.json', 'r') as fp:
        axisPara = json.load(fp)
    processor1.read_axis_raw(axisPara)
    print(processor1.axis)
    # processor1.set_zero(axisPara['axisDistances'][6])
    # for ii in range(len(axisPara['axisDistances'])):
    #     f = processor1.get_angle(axisPara['axisDistances'][ii])
    #     print(f)
    # f = processor1.get_angle([-8.49368, 15.76662, -37.0285])
    # print(f)
