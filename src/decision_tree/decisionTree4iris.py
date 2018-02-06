# -*- coding: utf-8 -*-
#
# copyright Kawa Yg
#

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier


def irisType(s):
    it = {b'Iris-setosa': 0, b'Iris-versicolor': 1, b'Iris-virginica': 2}
    return it[s]

isriFeature = u'花萼长度', u'花萼宽度', u'花瓣长度', u'花瓣宽度'

if __name__ == '__main__':

    data = np.loadtxt('iris.data', dtype=float, delimiter=',', converters={4: irisType})
    dataX, dataY = np.split(data, (4,), axis=1)
    dataX = dataX[:, :4]
    xtrain, xtest, ytrain, ytest = train_test_split(dataX, dataY, test_size=0.3, random_state=1)
    ytest = ytest.reshape(-1)

    # 测试最优depth
    depth = np.arange(1, 10)
    for d in depth:
        model = Pipeline([
            # 归一化特征
            ('ss', StandardScaler()),
            # Supported criteria are "gini" for the Gini impurity
            # and "entropy" for the information gain.
            ('DTC', DecisionTreeClassifier(criterion='entropy', max_depth=d))
        ])
        model = model.fit(xtrain, ytrain)
        ytestHat = model.predict(xtest)
        result = (ytestHat == ytest)
        accuracy = np.mean(result)
        print(d, u' depth 准确率： %.4f%%' % (100 * accuracy))
