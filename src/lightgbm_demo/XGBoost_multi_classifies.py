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

# label need to be 0 to num_class -1
# if col 33 is '?' let it be 1 else 0, col 34 substract 1
data = np.loadtxt('./dermatology.data', delimiter=',',converters={33: lambda x:int(x == '?'), 34: lambda x:int(x)-1 } )
sz = data.shape

train = data[:int(sz[0] * 0.7), :] # take row 1-256 as training set
test = data[int(sz[0] * 0.7):, :]  # take row 257-366 as testing set

train_X = train[:,0:33]
train_Y = train[:, 34]


test_X = test[:,0:33]
test_Y = test[:, 34]

xg_train = xgb.DMatrix( train_X, label=train_Y)
xg_test = xgb.DMatrix(test_X, label=test_Y)
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
pred = bst.predict( xg_test );

print ('predicting, classification error=%f' % (sum( int(pred[i]) != test_Y[i] for i in range(len(test_Y))) / float(len(test_Y)) ))

# do the same thing again, but output probabilities
param['objective'] = 'multi:softprob'
bst = xgb.train(param, xg_train, num_round, watchlist );
# Note: this convention has been changed since xgboost-unity
# get prediction, this is in 1D array, need reshape to (ndata, nclass)
yprob = bst.predict( xg_test ).reshape( test_Y.shape[0], 6 )
ylabel = np.argmax(yprob, axis=1)  # return the index of the biggest pro

print ('predicting, classification error=%f' % (sum( int(ylabel[i]) != test_Y[i] for i in range(len(test_Y))) / float(len(test_Y)) ))
