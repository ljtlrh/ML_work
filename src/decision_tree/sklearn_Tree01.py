# -*- coding: utf-8 -*-
'''
Created on  : 20180205
@author: ljt
决策树：
'''
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

filepath = "../data/ljt_train_dx.txt"

def isNone(d):
    from operator import eq as cmp
    return (d is None or cmp(d, 'None') or
                    cmp(d, '?') or
                    cmp(d, '') or
                    cmp(d, 'NULL') or
                    cmp(d, 'null'))

def is_empty_data_delet(curLine):
    sum = 0.0
    if isinstance(curLine, list):
        for itrm in curLine:
            if isNone(itrm):
                itrm=0.0
            else:
                sum += float(itrm)
    if sum > 0:
        return False
    else:
        return True

def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open(filepath)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        if is_empty_data_delet(curLine):
            continue
        lineArr = []
        size = len(curLine)
        for i in range(size):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(lineArr[-1]))
    return dataMat,labelMat



def dx_train():
    from sklearn import tree
    data, target = loadDataSet()
    dxFeature = ["judgedoc_is_no", "judgedoc_cnt", "litigant_defendant_cnt", "near_3_year_judgedoc_cnt",
                 "near_2_year_judgedoc_cnt", "near_1_year_judgedoc_cnt", "litigant_defendant_contract_dispute_cnt",
                 "litigant_defendant_bust_cnt", "litigant_defendant_infringe_cnt",
                 "litigant_defendant_Intellectual_property_owner_cnt", "litigant_defendant_unjust_enrich_cnt",
                 "litigant_result_sum_money", "net_judgedoc_defendant_cnt",
                 "shixin_is_no", "shixin_cnt", "near_3_year_shixin_cnt", "near_2_year_shixin_cnt",
                 "near_1_year_shixin_cnt", "court_announce_is_no",
                 "court_announce_cnt", "court_announce_litigant_cnt", "court_notice_is_no", "court_notice_cnt",
                 "court_notice_litigant_cnt"]
    feature_names = np.array(dxFeature)
    tarrget = [0, 1]
    target_names = np.array(tarrget)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(data, target)
    from sklearn.externals import joblib
    #保存模型
    joblib.dump(clf, "dx_train_model.m")
    # clf = joblib.load("train_model.m")
    import graphviz
    dot_data = tree.export_graphviz(clf, out_file=None,  # doctest: +SKIP
                                         feature_names=feature_names,  # doctest: +SKIP
                                         class_names=target_names,  # doctest: +SKIP
                                         filled=True, rounded=True,  # doctest: +SKIP
                                         special_characters=True)  # doctest: +SKIP
    graph = graphviz.Source(dot_data)  # doctest: +SKIP
    graph.render("dx_fid01")

def test03():
    '''
    DecisionTreeClassifier 既能用于二分类（其中标签为[-1,1]）也能用于多分类（其中标签为[0,…,k-1]）。
    使用Lris数据集，我们可以构造一个决策树，如下所示:
    :return:
    '''
    from sklearn.datasets import load_iris
    from sklearn import tree
    iris = load_iris()
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(iris.data, iris.target)
    import graphviz
    # dot_data = tree.export_graphviz(clf, out_file=None)
    # graph = graphviz.Source(dot_data)
    # graph.render("iris")
    print(iris.target_names)
    dot_data = tree.export_graphviz(clf, out_file=None,  # doctest: +SKIP
                                         feature_names=iris.feature_names,  # doctest: +SKIP
                                         class_names=iris.target_names,  # doctest: +SKIP
                                         filled=True, rounded=True,  # doctest: +SKIP
                                         special_characters=True)  # doctest: +SKIP
    graph = graphviz.Source(dot_data)  # doctest: +SKIP
    graph.render("iris02")  # doctest: +SKIP





def test02():
    import numpy as np
    import matplotlib.pyplot as plt

    from sklearn.datasets import load_iris
    from sklearn.tree import DecisionTreeClassifier

    # Parameters
    n_classes = 3
    plot_colors = "bry"
    plot_step = 0.02

    # Load data
    iris = load_iris()

    for pairidx, pair in enumerate([[0, 1], [0, 2], [0, 3],
                                    [1, 2], [1, 3], [2, 3]]):
        # We only take the two corresponding features
        X = iris.data[:, pair]
        y = iris.target

        # Train
        clf = DecisionTreeClassifier().fit(X, y)

        # Plot the decision boundary
        plt.subplot(2, 3, pairidx + 1)

        x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
        y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
                             np.arange(y_min, y_max, plot_step))

        Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)
        cs = plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)

        plt.xlabel(iris.feature_names[pair[0]])
        plt.ylabel(iris.feature_names[pair[1]])
        plt.axis("tight")

        # Plot the training points
        for i, color in zip(range(n_classes), plot_colors):
            idx = np.where(y == i)
            plt.scatter(X[idx, 0], X[idx, 1], c=color, label=iris.target_names[i],
                        cmap=plt.cm.Paired)

        plt.axis("tight")

    plt.suptitle("Decision surface of a decision tree using paired features")
    plt.legend()
    plt.show()

def test01():
    def irisType(s):
        it = {b'Iris-setosa': 0, b'Iris-versicolor': 1, b'Iris-virginica': 2}
        return it[s]

    isriFeature = u'花萼长度', u'花萼宽度', u'花瓣长度', u'花瓣宽度'
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
        ytestProba = model.predict_proba(xtest)
        print(ytestProba)
        result = (ytestHat == ytest)
        accuracy = np.mean(result)
        print(d, ' depth 准确率： %.4f%%' % (100 * accuracy))


if __name__ == '__main__':
    # test03()
    dx_train()