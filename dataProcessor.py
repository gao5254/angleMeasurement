import numpy as np
from PyQt5.QtCore import QObject


class dataProcessor(QObject):
    def __init__(self):  # 构造函数
        self.cPara = {
            "parallelRatio": [1, 1, 1],
            "frontOffset": [1, 1, 1],
            "xyCoordinate": [[1, 1], [1, 1], [1, 1]]
        }
        self.zeroDistances = 0
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
            'zeroDistances': self.zeroDistances,
            'zeroVector': self.zeroVector.tolist(),
            'axis': self.axis.tolist()
        }
        return axisPara

    def get_corrected_distances(self, distances: list) -> list:
        '''接口函数，计算校正后的距离值
        供主程序调用，传入原始距离值，返回校正后距离值
        '''
        NewDistances = [k*x + b for x, k, b in zip(distances, self.cPara['parallelRatio'], self.cPara['frontOffset'])]
        # NewDistances[0] = distances[0] * self.cPara['parallelRatio'][
        #     0] + self.cPara['frontOffset'][0]
        # NewDistances[1] = distances[1] * self.cPara['parallelRatio'][
        #     1] + self.cPara['frontOffset'][1]
        # NewDistances[2] = distances[2] * self.cPara['parallelRatio'][
        #     2] + self.cPara['frontOffset'][2]
        return NewDistances

    def set_zero(self, distances: list) -> bool:
        '''接口函数，设置零位面
        供主程序调用，传入一个包含三个距离值的列表，计算零位面的位置并记录在类内部，返回是否成功设置
        '''
        self.zeroDistances = distances[0]
        ZeroVector = self.get_vector(distances)
        ZeroVector = np.array(ZeroVector)
        self.zeroVector = np.transpose(ZeroVector)
        return True

    def get_vector(self, distances: list):
        # 输入三个Z值，求取归一化法向量
        RightDistances = self.get_corrected_distances(distances)
        point1 = self.cPara['xyCoordinate'][0] + [RightDistances[0]]
        point1 = np.array(point1)
        point2 = self.cPara['xyCoordinate'][1] + [RightDistances[1]]
        point2 = np.array(point2)
        point3 = self.cPara['xyCoordinate'][2] + [RightDistances[2]]
        point3 = np.array(point3)

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
        if 'zeroDistances' in axisPara and 'zeroVector' in axisPara and 'axis' in axisPara:
            self.zeroDistances = axisPara['zeroDistances']
            self.zeroVector = np.array(axisPara['zeroVector'])
            self.axis = np.array(axisPara['axis'])
            return True
        else:
            return False

    def set_axis2(self, distancesList: list) -> bool:
        n=len(distancesList)
        nrows=3
        ncols=n
        array=[[1]*nrows]*ncols
        #求取最小二乘法G矩阵
        for i in range(n):
            #array[i]=self.get_corrected_distances(distancesList[i])
            array[i]=self.get_vector(distancesList[i])
        #将列表转化为矩阵
        y1=[[1]*1]*ncols
        a=[[-1]*1]*ncols
        a=np.array(a)
        #a=np.transpose(a)
        y=np.array(y1)
        A=np.array(array)
        # A=np.transpose(A)
        # A=np.dot(self.a,A)
        # A=np.transpose(A)#n*3
        A1=A[:,0:2]
        A1=np.append(A1, a, axis=1)
        y=-100*A[:,2]
        At=np.transpose(A1) #转置
        #y=np.transpose(y2)#转置
        #最小二乘法求旋转轴
        X=np.dot(np.dot(np.linalg.inv(np.dot(At,A1)),At),y)
        #旋转轴乘以旋转矩阵，并归一化
        #X=np.transpose(X)
        #X=np.dot(a,X)
        #X=np.transpose(X)
        #sum1=math.sqrt(X[0]**2+X[1]**2+X[2]**2)
        #self.axis[0]=X[0]/sum1
        #self.axis[1]=X[1]/sum1
        #self.axis[2]=X[2]/sum1
        realaxis=X[0:2]
        realaxis=np.append(realaxis, [100], axis=0)
        #q=np.dot(np.linalg.inv(self.a),realaxis)
        y=np.linalg.norm(realaxis, axis=0, keepdims=True)
        self.axis=realaxis/y
        return True

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

    def get_angle(self, distances: list) -> float:
        '''接口函数，完成角度计算
        供主程序调用，传入一个包含三个距离值的列表，根据标定参数、旋转轴、零位面计算旋转角度，返回计算得到的角度
        '''
        vector = self.get_vector(distances)
        # vector = np.array(vector)
        # vector=np.transpose(vector)
        # axis=np.array(self.axis)
        # newvector = np.dot(self.RotationMatrix, vector)
        # newzero_vector = np.dot(self.RotationMatrix, self.zeroVector)
        # newvector = vector
        # newzero_vector = self.zeroVector
        # self.axis = self.axis.reshape(3)
        NormalVector1 = np.cross(vector, self.axis)  # 向量叉乘
        NormalVector2 = np.cross(self.zeroVector, self.axis)  # 向量叉乘
        # NormalVector1Length = np.sqrt(NormalVector1.dot(NormalVector1))
        # NormalVector2Length = np.sqrt(NormalVector2.dot(NormalVector2))
        NormalVector1Length = np.linalg.norm(NormalVector1)
        NormalVector2Length = np.linalg.norm(NormalVector2)

        cos_angle = NormalVector1.dot(NormalVector2) / (NormalVector1Length *
                                                        NormalVector2Length)
        angle = np.arccos(cos_angle)
        angle = angle * 180 / np.pi
        # 判断distances第一个点正负
        if distances[0] < self.zeroDistances:
            angle = -1 * angle
        return angle


# 实例
if __name__ == "__main__":
    processor1 = dataProcessor()
    a = processor1.set_calib_para({
        "parallelRatio": [1.0032464383880204,
        1.0006628010117244,
        1.0018212851273283],
        "frontOffset": [-0.087369469061961524,
        0.044005986644371831,
        0.043363482417589694],
        "xyCoordinate": [[
            -0.26299022917343962,
            119.68114118793503
        ],
        [
            -60.679538974097966,
            -0.064027064808072964
        ],
        [
            60.679538974097966,
            0.064027064808087175
        ]]
    })
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
    processor1.read_axis(axisPara)
    f = processor1.get_angle([1.07521,10.7875,-9.66941])
    print(f)

