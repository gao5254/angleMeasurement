# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 09:52:50 2020

@author: baoqi
"""

import numpy as np
from scipy.optimize import least_squares
import json
from dataProcessorAngleT import dataProcessor
import matplotlib.pyplot as plt


COUNTER = 0


def array2json(calibParaArray):

    calibParaJson = {
        "Angle": [0.0, 0.0, 0.0] + calibParaArray[0:6].tolist(),
        "T": [0.0, 0.0, 0.0] + calibParaArray[6:12].tolist(),
        "portNum": [5, 3, 4]
    }
    return calibParaJson


def residual(calibParaArray, axisParaList, sampleList, trueAngleList):
    global COUNTER
    COUNTER += 1
    print(COUNTER)

    calibParaJson = array2json(calibParaArray)

    resList = []
    num = len(axisParaList)
    for i in range(num):
        processor = dataProcessor()
        processor.set_calib_para(calibParaJson)
        processor.set_axis_SVD(axisParaList[i]["axisDistances"])
        processor.set_zero(axisParaList[i]["axisDistances"][6])
        angles = processor.get_angle(sampleList[i])
        res = trueAngleList[i] - angles
        resList.append(res)

    return np.concatenate(resList)


def readfile(calibFile, axisFileList):
    with open(calibFile, 'r') as fp:
        calibPara = json.load(fp)

    calibParaArray = np.empty((12, ))
    calibParaArray[0:6] = np.array(calibPara["Angle"][3:9])
    calibParaArray[6:12] = np.array(calibPara["T"][3:9])

    axisParaList = []
    sampleList = []
    trueAngleList = []
    for axisFile in axisFileList:
        with open(axisFile, 'r') as fp:
            axisPara = json.load(fp)
            axisParaList.append(axisPara)

        processor = dataProcessor()
        processor.set_calib_para(calibPara)
        processor.set_axis_SVD(axisPara["axisDistances"])
        processor.set_zero(axisPara["axisDistances"][6])
        values = np.array(axisPara["axisDistances"])
        sampleList.append(values)
        angles = processor.get_angle(values)
        angles = np.around(angles)
        trueAngleList.append(angles)

    return calibParaArray, axisParaList, sampleList, trueAngleList


calibFile = 'calibParaAngleT1.json'
axisFileList = ["axisPara1.json", "axisPara2.json", "axisPara3.json",
                "axisPara4.json", "axisPara5.json", "axisPara6.json"]
calibParaArray, axisParaList, sampleList, trueAngleList = readfile(
    calibFile, axisFileList)
a = residual(calibParaArray, axisParaList, sampleList, trueAngleList)

calibParaArrayRefine = least_squares(
    residual, calibParaArray, args=(
        axisParaList, sampleList, trueAngleList),
    method='lm', verbose=1, max_nfev=100000, xtol=1e-15, ftol=1e-15)

calibParaJsonRefine = array2json(calibParaArrayRefine.x)

with open('calibParaAngleTRefine1.json', 'w') as fp:
    json.dump(calibParaJsonRefine, fp, indent=4)
b = residual(calibParaArrayRefine.x, axisParaList, sampleList, trueAngleList)

plt.figure()
plt.plot(a)
plt.plot(b)
