# coding=utf8
'''
Created on 2018.02.27

@author:  
'''
import math
import random
import string
import numpy
import sys

random.seed(0)


def regularize(xMat):
    # inMat = xMat.copy()
    inMeans = numpy.mean(xMat, 0)
    inVar = numpy.var(xMat, 0)
    xMat = (xMat - inMeans) / inVar

    return xMat



def loadData(fileName):
    numFeat = len(open(fileName).readline().strip().split('\t')) - 1
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        if curLine[0] == '800':
            continue
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat


# 生成区间[a, b)内的随机数


def rand(a, b):
    return (b - a) * random.random() + a


def sigmoid(x):
    a = 1 / (1 + numpy.exp(-x))
    return a
    # return math.tanh(x)


# 函数 sigmoid 的派生函数, 为了得到输出 (即：y)


def dsigmoid(y):
    # return 1.0 - y**2
    return y * (1 - y)


class NN:
    def __init__(self, ni, nh, no):
        # 输入层、隐藏层、输出层的节点（数）
        self.input_num = ni + 1  # 增加一个偏差节点
        self.hide_num = nh
        self.output_num = no

        # 激活神经网络的所有节点（向量）
        self.input_arr = [1.0] * self.input_num
        self.hide_arr = [1.0] * self.hide_num
        self.output_arr = [1.0] * self.output_num

        # 建立权重（矩阵）
        self.inHide_weight = numpy.ones((self.input_num, self.hide_num)).tolist()
        self.hideOut_weight = numpy.ones((self.hide_num, self.output_num)).tolist()
        # 设为随机值
        for i in range(self.input_num):
            for j in range(self.hide_num):
                self.inHide_weight[i][j] = rand(-1.0, 1.0)
        for j in range(self.hide_num):
            for k in range(self.output_num):
                self.hideOut_weight[j][k] = rand(-1.0, 1.0)

    def update(self, inputs):

        # 激活输入层
        for i in range(self.input_num - 1):
            self.input_arr[i] = inputs[i]

        # 激活隐藏层
        for j in range(self.hide_num):
            sum1 = 0.0
            for i in range(self.input_num):
                sum1 = sum1 + self.input_arr[i] * self.inHide_weight[i][j]
            self.hide_arr[j] = sigmoid(sum1)

        # 激活输出层
        for k in range(self.output_num):
            sum2 = 0.0
            for j in range(self.hide_num):
                sum2 = sum2 + self.hide_arr[j] * self.hideOut_weight[j][k]
            self.output_arr[k] = sigmoid(sum2)

        return self.output_arr[:]

    def backPropagate(self, targets, N):
        ''' 反向传播 '''

        # 计算输出层的误差
        errorlist = [0.0] * self.output_num
        for k in range(self.output_num):
            error = targets[k] - self.output_arr[k]
            errorlist[k] = dsigmoid(self.output_arr[k]) * error

        # 计算隐藏层的误差
        hide_errlist = [0.0] * self.hide_num
        for j in range(self.hide_num):
            error = 0.0
            for k in range(self.output_num):
                error = error + errorlist[k] * self.hideOut_weight[j][k]
            hide_errlist[j] = dsigmoid(self.hide_arr[j]) * error

        # 更新输出层权重
        for j in range(self.hide_num):
            for k in range(self.output_num):
                change = errorlist[k] * self.hide_arr[j]
                self.hideOut_weight[j][k] = self.hideOut_weight[j][k] + N * change
        # 更新输入层权重
        for i in range(self.input_num):
            for j in range(self.hide_num):
                change = hide_errlist[j] * self.input_arr[i]
                self.inHide_weight[i][j] = self.inHide_weight[i][j] + N * change

        # 计算误差
        error = 0.0
        n = len(targets)
        for k in range(n):
            error = error + 0.5 * (targets[k] - self.output_arr[k]) ** 2
        # 计算系数
        pred = targets
        y_test = self.output_arr
        predsum = ((n * sum(pred ** 2) - sum(pred)** 2) * (n * sum(y_test ** 2) - sum(y_test) ** 2))
        testpre = (n * sum(pred * y_test) - sum(pred))**2
        R = (testpre / predsum) ** 2
        print(R)
        return error

    def test(self, xArr, yArr):
        count = 0
        for i in range(len(yArr)):
            y1 = self.update(xArr[i])[0]
            y2 = yArr[i]
            print(y2, '->', y1)

            if (y1 >= 0.5) and (y2 >= 0.0):
                count += 1
            if (y1 < 0.5) and (y2 < 0.0):
                count += 1

            # if abs(y1 - y2) < 1:
            #   count += 1;

        return count

    # 返回预测的y与正确的count值
    def testP(self, xArr, yArr):
        count = 0
        predict = []
        for i in range(len(yArr)):
            y1 = self.update(xArr[i])[0]
            y2 = yArr[i]
            print(y2, '->', y1)

            predict.append(y1)
            if (y1 >= 0.5) and (y2 >= 0.0):
                count += 1
            if (y1 < 0.5) and (y2 < 0.0):
                count += 1

            # if abs(y1 - y2) < 1:
            #   count += 1;

        return count, predict

    def train(self, xArr, yArr, iterations=1000, N=0.01):
        # N: 学习速率(learning rate)
        for i in range(iterations):
            error = 0.0
            for j in range(len(yArr)):
                inputs = xArr[j]

                targets = []
                targets.append(yArr[j])

                self.update(inputs)
                error = error + self.backPropagate(targets, N)
            if i % 100 == 0:
                print('err %-.5f' % error)


def testMain():
    xArr, yArr = loadData('data.txt')
    # print xArr
    # print xArr
    # xArr = regularize(xArr).tolist()
    n = NN(2, 10, 1)
    # 用一些模式训练它
    n.train(xArr[0:159][:], yArr[0:159])
    # 测试训练的成果
    print(n.test(xArr[160:200][:], yArr[160:200]))
    # 看看训练好的权重（当然可以考虑把训练好的权重持久化）
    print(n.weights())

import random
random.seed(0)

def rand(a, b):  # 随机函数
    return (b - a) * random.random() + a

def make_matrix(m, n, fill=0.0):  # 创建一个指定大小的矩阵
    mat = []
    for i in range(m):
        mat.append([fill] * n)
    return mat

# 定义sigmoid函数和它的导数
def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def sigmoid_derivate(x):
    return x * (1 - x)  # sigmoid函数的导数

class BPNeuralNetwork:
    def __init__(self):
        #初始化变量
        self.input_n = 0
        self.hidden_n = 0
        self.output_n = 0
        self.input_cells = []
        self.hidden_cells = []
        self.output_cells = []
        self.input_weights = []
        self.output_weights = []
        self.input_correction = []
        self.output_correction = []

    # 三个列表维护：输入层，隐含层，输出层神经元
    def setup(self,ni,nh,no):
        self.input_n = ni + 1 # 输入层+偏置项
        self.hidden_n = ni + 1 # 隐含层
        self.output_n = ni + 1 # 输出层

        #初始化神经元
        self.input_cells = [1.0]*self.input_n
        self.hidden_cells = [1.0]*self.hidden_n
        self.output_cells = [1.0]*self.output_n
        # 初始化连接边的权重
        self.input_weights = make_matrix(self.input_n, self.hidden_n) #邻接矩阵存边权：输入层->隐藏层
        self.output_weights = make_matrix(self.hidden_n, self.output_n) #邻接矩阵存边权：隐藏层->输出层





if __name__ == '__main__':
    testMain()
