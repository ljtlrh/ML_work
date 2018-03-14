#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 18-3-13 下午4:49
# @Author  : liujiantao
# @Site    : 
# @File    : XGBoost_multi_classifies.py
# @Software: PyCharm
'''
   XGBoost官方给的二分类问题的例子是区别蘑菇有无毒，数据集和代码都可以在xgboost中的demo文件夹对应找到，我是用的Anaconda安装的XGBoost，实现起来比较容易。唯一的梗就是在终端中运行所给命令：  ../../xgboost mushroom.conf 时会报错，是路径设置的问题，所以我干脆把xgboost文件夹下的xgboost.exe拷到了mushroom.conf配置文件所在文件夹下，这样直接定位到该文件夹下就可以运行： xgboost mushroom.conf。二分类数据预处理，也就是data wraggling部分的代码有一定的借鉴意义，值得一看。
    多分类问题给的例子是根据34个特征识别6种皮肤病，由于终端中运行runexp.sh没有反应，也不报错，所以我干脆把数据集下载到对应的demo文件夹下了,主要的代码如下，原来有部分比较难懂的语句我自己加了一些注释，这样理解起来就会顺畅多了。
'''

#! /usr/bin/python
import numpy as np
import xgboost as xgb

filepath00 = "recomend_h_cluster_users.csv"

def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open(filepath00)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        # 调整正负样本比例
        size = len(curLine)
        lineArr = []
        label = str(curLine[6])
        for i in range(size - 1):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(label)
    # try:
    #     np.savetxt("dataMat_train.txt", dataMat, delimiter=',')
    #     np.savetxt("data_labelMat_train.txt", labelMat)
    #     dataMat = np.loadtxt("dataMat_train.txt", delimiter=',')
    #     dataMat = dataMat.tolist()
    #     labelMat = np.loadtxt("data_labelMat_train.txt", delimiter=',')
    #     labelMat = labelMat.tolist()
    # except :
    #     print ("fffff")
    return dataMat, labelMat
def dealdata(X, y):
    '''
    train_test_split(train_data,train_target,test_size=0.4, random_state=0)
    train_data：所要划分的样本特征集
    train_target：所要划分的样本结果
    test_size：样本占比，如果是整数的话就是样本的数量
    random_state：是随机数的种子。
    随机数种子：其实就是该组随机数的编号，在需要重复试验的时候，保证得到一组一样的随机数。比如你每次都填1，
    其他参数一样的情况下你得到的随机数组是一样的。但填0或不填，每次都会不一样。
    随机数的产生取决于种子，随机数和种子之间的关系遵从以下两个规则：
    种子不同，产生不同的随机数；种子相同，即使实例不同也产生相同的随机数。
    :param X:
    :param y:
    :return:
    '''
    from sklearn.model_selection import train_test_split
    # 随机抽取20%的测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)
    return X_train, X_test, y_train, y_test
# label need to be 0 to num_class -1
# if col 33 is '?' let it be 1 else 0, col 34 substract 1
# data = np.loadtxt('./recomend_h_cluster_users.csv', delimiter=',',converters={33: lambda x:int(x == '?'), 34: lambda x:int(x)-1 } )
# data = np.loadtxt('./recomend_h_cluster_users.csv', delimiter=',')
# sz = data.shape
# train = data[:int(sz[0] * 0.7), :] # take row 1-256 as training set
# test = data[int(sz[0] * 0.7):, :]  # take row 257-366 as testing set


# train_X = train[:, 0:6]
# train_Y = train[:, 7]
#
#
# test_X = test[:, 0:6]
# test_Y = test[:, 7]
data, target = loadDataSet()
X_train, X_test, y_train, test_Y = dealdata(data, target)

xg_train = xgb.DMatrix(X_train, label=y_train)
xg_test = xgb.DMatrix(X_test, label=test_Y)
# setup parameters for xgboost
param = {}
# use softmax multi-class classification
param['objective'] = 'multi:softmax'
# scale weight of positive examples
param['eta'] = 0.1
param['max_depth'] = 6
param['silent'] = 1
param['nthread'] = 4
param['num_class'] = 6

watchlist = [ (xg_train,'train'), (xg_test, 'test') ]
num_round = 5
bst = xgb.train(param, xg_train, num_round, watchlist );
# get prediction
pred = bst.predict(xg_test)

print ('predicting, classification error=%f' % (sum( int(pred[i]) != test_Y[i] for i in range(len(test_Y))) / float(len(test_Y)) ))

# do the same thing again, but output probabilities
param['objective'] = 'multi:softprob'
bst = xgb.train(param, xg_train, num_round, watchlist );
# Note: this convention has been changed since xgboost-unity
# get prediction, this is in 1D array, need reshape to (ndata, nclass)
yprob = bst.predict( xg_test ).reshape( test_Y.shape[0], 6 )
ylabel = np.argmax(yprob, axis=1)  # return the index of the biggest pro

print ('predicting, classification error=%f' % (sum( int(ylabel[i]) != test_Y[i] for i in range(len(test_Y))) / float(len(test_Y)) ))
