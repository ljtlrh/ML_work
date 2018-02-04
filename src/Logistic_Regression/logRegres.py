
from numpy import *
import numpy as np
import math
import time
from operator import eq as cmp
import pandas as pd


filepath = "../data/ljt_train_dx.txt"
def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open(filepath)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        lineArr = []
        for i in range(21):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[21]))
    return dataMat, labelMat

def loadcsv(path):
    ''''''
    frame = pd.read_csv(path)
    print(frame.head())
    dfvalues01 = frame.values
    dfvshap01 = np.shape(dfvalues01)
    dfrows = dfvshap01[0]
    dfcols = dfvshap01[1]
    company_name = list(frame['company_name'].values)
    dataMat = frame
    labelMat = frame
    return dataMat, labelMat

def isNone(d):
    return (d is None or cmp(d, 'None') or
                    cmp(d, '?') or
                    cmp(d, '') or
                    cmp(d, 'NULL') or
                    cmp(d, 'null'))

def dealdata(X, y):
    from sklearn.model_selection import train_test_split
    # 随机抽取20%的测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    return X_train, X_test, y_train, y_test
# Type converter
def initData(d01):
    shape01 = np.shape(d01)
    if shape01:
        return 0
    row01 = shape01[0]
    col01 = shape01[1]
    for i in range(0, row01):
        for j in range(0, col01):
            d = d01[i][j]
            if (d is None or cmp(d, 'None') or
                    cmp(d, '?') or
                    cmp(d, '') or
                    cmp(d, 'NULL') or
                    cmp(d, 'null')):
                d01[i][j] = 0.0
    return d01

def sigmoid(inX):
    return 1.0/(1+exp(-inX))

def gradAscent(dataMat, classLabel):
    dataMatrix = mat(dataMat)
    labelMat = mat(classLabel).transpose()
    m,n = shape(dataMatrix)
    alpha = 0.001
    maxCycles = 500
    weights = ones((n, 1))
    for k in range(maxCycles):
        h = sigmoid(dataMatrix * weights)
        error = (labelMat - h)
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights

'''
    随机梯度上升：
    由一个样本点来更新数据，是增量式更新，所以是一个在线学习算法（与之对应的是一次处理所有样本数据的批处理）
'''
def stocGradAscent0(dataMatrix, classLabel):
    m,n = shape(dataMatrix)
    alpha = 0.01
    weights = ones(n)
    for i in range(m):
        h = sigmoid(sum(dataMatrix[i]*weights))
        error = classLabel[i] - h
        weights = weights + alpha * error * dataMatrix[i]
    return weights

'''
    改进版随机梯度算法
'''
def stocGradAscent1(dataMatrix, classLabel, numIter=150):
    m,n = shape(dataMatrix)
    weights = ones(n)
    for j in range(numIter):
        dataIndex = list(range(m))
        for i in range(m):
            alpha = 4/(1.0+i+j)+0.01
            randIndex = int(random.uniform(0, len(dataIndex)))
            h = sigmoid(sum(dataMatrix[randIndex]*weights))
            error = classLabel[randIndex] - h
            weights = weights + alpha * error * dataMatrix[randIndex]
            del(dataIndex[randIndex])
    return weights

def plotBestFit(weights):
    import matplotlib.pyplot as plt
    dataMat, labelMat = loadDataSet()
    dataAddr = array(dataMat)
    n = shape(dataAddr)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataAddr[i, 1])
            ycord1.append(dataAddr[i, 2])
        else:
            xcord2.append(dataAddr[i, 1])
            ycord2.append(dataAddr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = arange(-3.0, 3.0, 0.1)
    y = (-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x, y)
    plt.xlabel('X1')
    plt.ylabel('X2')
    plt.show()

def classifyVector(inX, weights):
    prob = sigmoid(sum(inX*weights))
    if prob > 0.5: return 1.0
    else: return 0.0

def colicTest():
    frTrain = open('horseColicTraining.txt')
    frTest = open('horseColicTest.txt')
    trainSet = []
    trainLabel = []
    for line in frTrain.readlines():
        curLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(curLine[i]))
        trainSet.append(lineArr)
        trainLabel.append(float(curLine[21]))
    trainWeight = stocGradAscent1(array(trainSet), trainLabel, 500)
    errorCount = 0
    numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        curLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(curLine[i]))
        if int(classifyVector(array(lineArr), trainWeight))!=int(curLine[21]):
            errorCount += 1
    errorRate = float(errorCount)/numTestVec
    print('the error rate of this test is：%f' % errorRate)
    return errorRate


def coliccsvTest():
    frTrain = open('horseColicTraining.txt')
    frTest = open('horseColicTest.txt')
    trainSet = []
    trainLabel = []
    for line in frTrain.readlines():
        curLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(curLine[i]))
        trainSet.append(lineArr)
        trainLabel.append(float(curLine[21]))
    trainWeight = stocGradAscent1(array(trainSet), trainLabel, 500)
    errorCount = 0
    numTestVec = 0.0
    for line in frTest.readlines():
        numTestVec += 1.0
        curLine = line.strip().split('\t')
        lineArr = []
        for i in range(21):
            lineArr.append(float(curLine[i]))
        if int(classifyVector(array(lineArr), trainWeight))!=int(curLine[21]):
            errorCount += 1
    errorRate = float(errorCount)/numTestVec
    print('the error rate of this test is：%f' % errorRate)
    return errorRate

def multiTest():
    numTests = 10
    errorSum = 0.0
    for k in range(numTests):
        errorSum += colicTest()
    print('after %d interations the average error rate is:%f'%(numTests, errorSum/float(numTests)))

def multiTest2():
    numTests = 10
    errorSum = 0.0
    for k in range(numTests):
        errorSum += coliccsvTest()
    print('after %d interations the average error rate is:%f'%(numTests, errorSum/float(numTests)))

if __name__ == "__main__":
    # data, label = loadDataSet()
    data, label = loadDataSet()
    weights = gradAscent(data, label)
    plotBestFit(weights.getA())
    weights = stocGradAscent0(array(data), label)
    plotBestFit(weights)
    weights = stocGradAscent1(array(data), label)
    plotBestFit(weights)
    # multiTest()
    # multiTest2()
