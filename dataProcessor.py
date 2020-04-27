from PyQt5.QtCore import QObject
import math
import numpy as np
class dataProcessor(QObject):
    def __init__(self):#构造函数
        self.cPara = {
            "parallelRatio":[1, 1, 1],
            "frontOffset":[1, 1, 1],
            "xyCoordinate":[[1, 1], [1, 1], [1, 1]]
        }
        self.zero_vector=np.array([[1],[1],[1]])
        self.axis=np.array([[1],[1],[1]])
        self.a=np.array([[1/(3**0.5),-1/(3**0.5),-1/(3**0.5)],[1/(6**0.5),2**0.5/3**0.5,-1/(6**0.5)],[1/(2**0.5),0,1/(2**0.5)]])

    def set_calib_para(self, calibPara):
        '''接口函数，设置标定参数
        供主程序调用，传入一个含有标定参数的字典，将其保存为类的内部成员变量，返回是否成功调用
        '''
        self.cPara=calibPara
        return True

    def get_corrected_distances(self, distances: list) -> list:
        '''接口函数，计算校正后的距离值
        供主程序调用，传入原始距离值，返回校正后距离值
        '''
        newdistances=[1,1,1]
        newdistances[0]=distances[0]*self.cPara['parallelRatio'][0]+self.cPara['frontOffset'][0]
        newdistances[1]=distances[1]*self.cPara['parallelRatio'][1]+self.cPara['frontOffset'][1]
        newdistances[2]=distances[2]*self.cPara['parallelRatio'][2]+self.cPara['frontOffset'][2]
        return newdistances

    def set_zero(self, distances: list) -> bool:
        '''接口函数，设置零位面
        供主程序调用，传入一个包含三个距离值的列表，计算零位面的位置并记录在类内部，返回是否成功设置
        '''
        a =self.get_vector(distances)
        a=np.array(a)
        self.zero_vector=np.transpose(a)
        return True

    def get_vector(self, distances: list):
        #输入三个Z值，求取归一化法向量
        dis=self.get_corrected_distances(distances)
        point1=self.cPara['xyCoordinate'][0]+[dis[0]]
        point2=self.cPara['xyCoordinate'][1]+[dis[1]]
        point3=self.cPara['xyCoordinate'][2]+[dis[2]]
        #三个点转化为两个向量
        vector1=[point2[0]-point1[0],point2[1]-point1[1],point2[2]-point1[2]]
        vector2=[point3[0]-point1[0],point3[1]-point1[1],point3[2]-point1[2]]
        #两个向量求法向量，并归一化
        normalvector=[1,1,1]
        newvector=[1,1,1]
        normalvector[0]=vector1[1]*vector2[2]-vector2[1]*vector1[2]
        normalvector[1]=vector1[0]*vector2[2]-vector2[0]*vector1[2]
        normalvector[2]=vector1[0]*vector2[1]-vector2[0]*vector1[1]
        sum=math.sqrt(normalvector[0]**2+normalvector[1]**2+normalvector[2]**2)
        newvector[0]=normalvector[0]/sum
        newvector[1]=normalvector[1]/sum
        newvector[2]=normalvector[2]/sum
        #返回归一化法向量
        return newvector

    def set_axis(self, distancesList: list) -> bool:
        '''接口函数，完成旋转轴标定过程
        供主程序调用，传入*二维列表*，进行旋转轴标定，并记录在类内部，返回是否成功设置
        '''
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
        A=np.transpose(A)
        A=np.dot(self.a,A)
        A=np.transpose(A)#n*3
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

    def get_angle(self, distances: list) -> float:
        '''接口函数，完成角度计算
        供主程序调用，传入一个包含三个距离值的列表，根据标定参数、旋转轴、零位面计算旋转角度，返回计算得到的角度
        '''
        #a=np.array([[1/(3**0.5),-1/(3**0.5),-1/(3**0.5)],[1/(6**0.5),2**0.5/3**0.5,-1/(6**0.5)],[1/(2**0.5),0,1/(2**0.5)]])
        vector=self.get_vector(distances)
        vector=np.array(vector)
        #vector=np.transpose(vector)
        #axis=np.array(self.axis)
        newvector=np.dot(self.a,vector)
        newzero_vector=np.dot(self.a,self.zero_vector)

        #a1=np.array(newvector)
        #b=np.array(newzero_vector)
        self.axis=self.axis.reshape(3)
        c=np.cross(newvector,self.axis)#向量叉乘
        d=np.cross(newzero_vector,self.axis)#向量叉乘
        c1=np.sqrt(c.dot(c))
        d1=np.sqrt(d.dot(d))
        cos_angle=c.dot(d)/(c1*d1)
        angle=np.arccos(cos_angle)
        angle=angle*360/2/np.pi
        return angle

#实例
if __name__ == "__main__":

    processor1=dataProcessor()
    a=processor1.set_calib_para({
            "parallelRatio":[1, 1, 1],
            "frontOffset":[0, 0, 0],
            "xyCoordinate":[[0, 0], [0, 1], [1, 0]]
        })
    print(a)
    b=processor1.get_corrected_distances([1,1,1])
    print(b)
    c=processor1.get_vector([1,1,1])
    print(c)
    d=processor1.set_zero([1,1,1])
    print(d)
    e=processor1.set_axis([[1.02,1,0.98],[1.01,0,0.99],[0.998,2,1.01],[1.01,3,0.997],[1.004,-1,0.996]])
    print(e)
    f=processor1.get_angle([1,2,1])
    print(f)
