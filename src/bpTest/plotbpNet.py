# coding=utf-8
'''
Created on 2016��5��17��

@author:
'''
from train.bpNet import *
import matplotlib.pyplot as plt
import sys


def testBestLearningRate():
    rate = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1]
    errNum = []
    for i in range(len(rate)):
        print('test' + str(i))
        xArr, yArr = loadData('data.txt')
        n = NN(2, 7, 1)
        # 用一些模式训练它
        n.train(xArr[0:159][:][:], yArr[0:159][:], 500, rate[i])
        errNum.append(n.test(xArr[0:159][:][:], yArr[0:159][:]))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    x1 = range(7)
    ax.plot(x1, errNum)
    plt.show()
    plt.savefig("LearningRate.png")


def testBestNumOfNeural():
    nums = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    errNum = []
    for i in range(len(nums)):
        print('test' + str(i))
        xArr, yArr = loadData('data.txt')
        n = NN(2, nums[i], 1)
        n.train(xArr[0:159][:][:], yArr[0:159][:], 500)
        errNum.append(n.test(xArr[0:159][:][:], yArr[0:159][:]))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(nums, errNum)
    plt.show()
    plt.savefig("predict_erro01.png")


def testNorm():
    xArr, yArr = loadData('data.txt')
    # print xArr
    # print xArr
    xArr = regularize(xArr).tolist()
    n = NN(2, 7, 1)
    # 用一些模式训练它
    n.train(xArr[0:159][:][:], yArr[0:159][:], 500, 0.01)
    print(n.test(xArr[0:159][:][:], yArr[0:159][:]))


def testNoNorm():
    xArr, yArr = loadData('data.txt')
    n = NN(2, 7, 1)
    # 用一些模式训练它
    n.train(xArr[0:159][:][:], yArr[0:159][:], 500, 0.01)
    print(n.test(xArr[0:159][:][:], yArr[0:159][:]))

def loadDataX(fileName):
    numFeat = len(open(fileName).readline().strip().split('\t')) - 1
    X = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
            X.append(lineArr)
        if curLine[0] == '800':
            break
    return X
def testPredict():
    xArr, yArr = loadData('data.txt')
    n = NN(2, 7, 1)
    # 用一些模式训练它
    n.train(xArr[0:159][:][:], yArr[0:159][:], 160, 0.01)
    count, predict = n.testP(xArr[160:200][:], yArr[160:200])
    print(count)
    x1 = loadDataX('data.txt')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x1, predict)
    plt.show()
    plt.savefig("predict01.png")




if __name__ == '__main__':
    # for arg in sys.argv:
    #     if arg == '-rate':
    #         testBestLearningRate()
    #     if arg == '-num':
    #         testBestNumOfNeural()
    #     if arg == '-predict':
    #         testPredict()
    #     if arg == '-norm':
    #         testNorm()
    #     if arg == '-nonorm':
    #         testNoNorm()
    testPredict()
