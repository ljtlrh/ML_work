#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 18-3-14 下午2:14
# @Author  : liujiantao
# @Site    : 
# @File    : Sklearn_multi_classfies.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
'''
Created on  : 20180208
@author: ljt
决策树：
'''
import numpy as np
from sklearn import tree
import matplotlib.pyplot as plt

target_names = ['HP0', 'HP1225', 'HP16', 'HP2000', 'HP2010', 'HP2074', 'HP78', 'HP820']

filepath00 = "recomend_h_cluster_users.csv"

dxFeature = ['UTag', 'TUTag', 'TagU', 'MonthU']

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
        # for i in range(size - 1):
        #     lineArr.append(float(curLine[i]))
        dataMat.append(curLine[1:5])
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

def isNone(d):
    from operator import eq as cmp
    return (d is None or d == 'None' or
                    d == '?' or
                    d == '' or
                    d == 'NULL' or
                    d == 'null')

def write_txt(path, data):
    '''
     保存清洗数据
    '''
    f = open(path, 'w')
    f.write(data.decode('unicode_escape'))
    f.write('\n')  # write不会在自动行末加换行符，需要手动加上
    f.flush()
    f.close()

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

def Recall(P,TP):
    '''
    计算推荐结果的召回率,原本为对的当中预测为对的比例
    :param P: POSITIVE 正样本
    :param TP: TRUE POSITIVE 真正，被模型预测为正测正样本
    :return:
    '''

    return TP / (P * 1.0)


def Precision(TP, FP):
    '''
    计算推荐结果的准确率，预测为对当中原本为对的的比例
    :param TP: TRUE POSITIVE 真正，被模型预测为正的正样本
    :param FP: False POSITIVE 假正，被模型预测为正样本的负样本
    :return:
    '''
    return TP / (TP*1.0 + FP*1.0)

def TP_RATE(P, TP):
    '''
    正确率：原本是对的预测为对的比率
    :param P:  正样本
    :param TP: 真正，被模型预测为正的正样本
    :return:
    '''
    return TP / (P*1.0)

def FP_RATE(N, FP):
    '''
    错误率：原本是错的预测为对的比率
    :param N:  负样本
    :param FP: 假正，被模型预测为正的负样本
    :return:
    '''
    return FP / (N*1.0)

def ROC_AUC(y, pred):
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve
    # y = np.array([1, 1, 2, 2])
    # pred = np.array([0.1, 0.4, 0.35, 0.8])
    fpr, tpr, thresholds = roc_curve(y, pred[:,1], pos_label=1)
    # print("正确率：fpr==>"+str(fpr))
    # print("错误率：tpr==>"+str(tpr))
    # print(thresholds)
    from sklearn.metrics import auc
    auc_area = auc(fpr, tpr)
    # 画图，只需要plt.plot(fpr,tpr),变量roc_auc只是记录auc的值，通过auc()函数能计算出来
    plt.plot(fpr, tpr, lw=1, label='ROC  (area = %0.2f)' % ( auc_area))
    print("auc_area:"+str(auc_area))
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.savefig("./sklearn_result01/aoc_fig.png")
    plt.show()

def feature_importance():

    from sklearn.ensemble import ExtraTreesClassifier
    data, target = loadDataSet()
    X_train, X_test, y_train, y_test = dealdata(data, target)

    forest = ExtraTreesClassifier(n_estimators=250,
                                  random_state=0)
    forest.fit(X_train, y_train)
    importances = forest.feature_importances_
    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]
    size = 25
    # Print the feature ranking
    print("Feature ranking:")

    for f in range(size-1):
        print("%d. %s: %d (%f)" % (f + 1, dxFeature[f], indices[f], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(size-1), importances[indices],
            color="r", yerr=std[indices], align="center")
    plt.xticks(range(size-1), indices)
    plt.xlim([-1, size-1])
    plt.show()

def dx_train():
    from sklearn import tree
    from sklearn import ensemble
    data, target = loadDataSet()
    X_train, X_test, y_train, y_test = dealdata(data, target)
    from sklearn.ensemble import ExtraTreesClassifier
    '''
    附加树分类器。
这个类实现了一个元估计适合许多随机决策树（又名多余的树木）的数据集，使用平均提高了拟合预测的精度和控制各子样本。
    '''
    clf = ExtraTreesClassifier(n_estimators=130,
                                  random_state=0)
    # from sklearn.ensemble import RandomForestClassifier
    # clf = RandomForestClassifier(criterion="entropy", n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
    '''
    决策树
    '''
    # clf = tree.DecisionTreeClassifier(max_depth=4, splitter="best",
    #                                   max_features=4, min_samples_split=4,
    #                                   max_leaf_nodes=4)

    # 测试最优depth
    # depth = np.arange(1, 10)
    # for d in depth:
    #     clf = Pipeline([
    #         # 归一化特征
    #         ('ss', StandardScaler()),
    #         # Supported criteria are "gini" for the Gini impurity
    #         # and "entropy" for the information gain.
    #         ('DTC', DecisionTreeClassifier(criterion='entropy', max_depth=d))
    #     ])
    clf = clf.fit(X_train, y_train)
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    size = len(dxFeature)
    # Print the feature ranking
    print(str(size)+" Feature ranking:")
    for f in range(size):
        print("feature name: %s <==> importances rate: (%f)" % (dxFeature[indices[f]], importances[indices[f]]))

    # from sklearn.externals import joblib
    # #保存模型
    # joblib.dump(clf, "./classfies_train_model.m", compress=3)
    # clf = joblib.load("./classfies_train_model.m")
    import graphviz
    feature_names = np.array(dxFeature)
    ytestPre= clf.predict(X_test)
    # result = (y_test == ytestPre)
    # accuracy = np.mean(result)
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(y_test, ytestPre)
    print(u'准确率： %.4f%%' % (100 * accuracy))
    from sklearn import metrics
    precision = metrics.precision_score(y_test, ytestPre, average='micro')  # 微平均，精确率
    print(u'微平均，精确率： %.4f%%' % (100 * precision))
    recall = metrics.recall_score(y_test, ytestPre, average='macro')
    print(u'微平均，召回率： %.4f%%' % (100 * recall))
    f1_score = metrics.f1_score(y_test, ytestPre, average='weighted')
    print(u'微平均，调和平均数： %.4f%%' % (100 * f1_score))
    from sklearn.metrics import classification_report
    print(classification_report(y_test, ytestPre, target_names=target_names))
    from sklearn.metrics import cohen_kappa_score
    kappa_score = cohen_kappa_score(y_test, ytestPre)
    print(u'kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： %.4f%%' % (100 * kappa_score))
    pre_result = clf.predict_proba(X_test)
    # ROC_AUC(y_test, pre_result)
    # dot_data = tree.export_graphviz(clf, out_file=None,  # doctest: +SKIP
    #                                      feature_names=feature_names,  # doctest: +SKIP
    #                                      class_names=target_names,  # doctest: +SKIP
    #                                      filled=True, rounded=True,  # doctest: +SKIP
    #                                      special_characters=True)
    # graph = graphviz.Source(dot_data)  # doctest: +SKIP
    # graph.render("./classfies_fig01")

def evaluate_function(clf,X_test,y_test):
    ytestPre = clf.predict(X_test)
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(y_test, ytestPre)
    print(u'准确率： %.4f%%' % (100 * accuracy))
    from sklearn import metrics
    precision = metrics.precision_score(y_test, ytestPre, average='micro')  # 微平均，精确率
    print(u'微平均，精确率： %.4f%%' % (100 * precision))
    recall = metrics.recall_score(y_test, ytestPre, average='macro')
    print(u'微平均，召回率： %.4f%%' % (100 * recall))
    f1_score = metrics.f1_score(y_test, ytestPre, average='weighted')
    print(u'微平均，调和平均数： %.4f%%' % (100 * f1_score))
    from sklearn.metrics import classification_report
    print(classification_report(y_test, ytestPre, target_names=target_names))
    from sklearn.metrics import cohen_kappa_score
    kappa_score = cohen_kappa_score(y_test, ytestPre)
    print(u'kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： %.4f%%' % (100 * kappa_score))
    pre_result = clf.predict_proba(X_test)
    ROC_AUC(y_test, pre_result)

def plot_fig(clf,figpath):
    import graphviz
    feature_names = np.array(dxFeature)
    dot_data = tree.export_graphviz(clf, out_file=None,  # doctest: +SKIP
                                         feature_names=feature_names,  # doctest: +SKIP
                                         class_names=target_names,  # doctest: +SKIP
                                         filled=True, rounded=True,  # doctest: +SKIP
                                         special_characters=True)
    graph = graphviz.Source(dot_data)  # doctest: +SKIP
    graph.render(figpath)

def dx_train2():

    from sklearn import ensemble
    data, target = loadDataSet()

    X_train, X_test, y_train, y_test = dealdata(data, target)
    from sklearn.ensemble import ExtraTreesClassifier
    '''
    附加树分类器。
    这个类实现了一个元估计适合许多随机决策树（又名多余的树木）的数据集，使用平均提高了拟合预测的精度和控制各子样本。
    '''
    clf = ExtraTreesClassifier(n_estimators=250,
                                  random_state=0,max_depth=60)
    # from sklearn.ensemble import RandomForestClassifier
    # clf = RandomForestClassifier(criterion="entropy", n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
    '''
    决策树
    '''
    # clf = tree.DecisionTreeClassifier(max_depth=60, splitter="best", criterion='entropy',
    #                                   max_features=60, min_samples_split=60,
    #                                   max_leaf_nodes=124)


    clf = clf.fit(X_train, y_train)
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    size = len(dxFeature)
    # Print the feature ranking
    print(str(size)+" criterion='gini', Feature ranking:")
    for f in range(size):
        print("feature name: %s <==> importances rate: (%f)" % (dxFeature[indices[f]], importances[indices[f]]))

    # from sklearn.externals import joblib
    # #保存模型
    # joblib.dump(clf, "./sklearn_result01/dx_train_model.m", compress=3)
    # clf = joblib.load("./sklearn_result01/dx_train_model.m")
    evaluate_function(clf, X_test, y_test)
    # plot_fig("./sklearn_result01/dx_fig01")

def sklearn_single_classficatopn_test():
    '''
     sklearn 大致可以将这些分类器分成两类：
     1）单一分类器
     2）集成分类器
    :return:
    '''
    data, target = loadDataSet()
    X_train, X_test, y_train, y_test = dealdata(data, target)
    from sklearn.model_selection import cross_val_score
    from sklearn.datasets import make_blobs
    # meta-estimator
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.ensemble import ExtraTreesClassifier
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.ensemble import GradientBoostingClassifier

    from sklearn.naive_bayes import GaussianNB
    from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
    from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
    classifiers = {
        'KN': KNeighborsClassifier(3),
        'SVC': SVC(kernel="linear", C=0.025),
        'SVC': SVC(gamma=2, C=1),
        'DT': DecisionTreeClassifier(max_depth=5),
        'RF': RandomForestClassifier(n_estimators=10, max_depth=5, max_features=1),  # clf.feature_importances_
        'ET': ExtraTreesClassifier(n_estimators=10, max_depth=None),  # clf.feature_importances_
        'AB': AdaBoostClassifier(n_estimators=100),
        'GB': GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0),
    # clf.feature_importances_
        'GNB': GaussianNB(),
        'LD': LinearDiscriminantAnalysis(),
        'QD': QuadraticDiscriminantAnalysis()}

    for name, clf in classifiers.items():
        clf = clf.fit(X_train, y_train)
        importances = clf.feature_importances_
        indices = np.argsort(importances)[::-1]
        size = len(dxFeature)
        # Print the feature ranking
        print(str(size)+" criterion='gini', Feature ranking:")
        for f in range(size):
            print("feature name: %s <==> importances rate: (%f)" % (dxFeature[indices[f]], importances[indices[f]]))

        # from sklearn.externals import joblib
        # #保存模型
        # joblib.dump(clf, "./sklearn_result01/dx_train_model.m", compress=3)
        # clf = joblib.load("./sklearn_result01/dx_train_model.m")
        evaluate_function(clf, X_test, y_test)
        # plot_fig("./sklearn_result01/dx_fig01")








def AdaBoost_dx_train():
    '''
    bagging 一种投票的思想
    :return:
    '''
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.tree import DecisionTreeClassifier
    data, target = loadDataSet()
    dataArr, testArr, classLabels, testLabelArr = dealdata(data, target)
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=2), algorithm="SAMME", n_estimators=10)
    # bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=20), n_estimators=600, learning_rate=1)
    bdt.fit(dataArr, classLabels)
    predictions = bdt.predict(dataArr)
    errArr = np.mat(np.ones((len(dataArr), 1)))
    print('训练集的错误率:%.3f%%' % float(errArr[predictions != classLabels].sum() / len(dataArr) * 100))
    predictions = bdt.predict(testArr)
    errArr = np.mat(np.ones((len(testArr), 1)))
    print('测试集的错误率:%.3f%%' % float(errArr[predictions != testLabelArr].sum() / len(testArr) * 100))
    importances = bdt.feature_importances_
    indices = np.argsort(importances)[::-1]
    size = len(dxFeature)
    # Print the feature ranking
    print("Feature ranking:")
    for f in range(size - 1):
        print("%d. %s: %d (%f)" % (f + 1, dxFeature[f], indices[f], importances[indices[f]]))

    # from sklearn.externals import joblib
    # #保存模型
    # joblib.dump(clf, "./sklearn_result01/dx_train_model.m", compress=3)
    # clf = joblib.load("./sklearn_result01/dx_train_model.m")
    import graphviz
    # feature_names = np.array(dxFeature)
    # TP = 0
    # FP = 0
    # TN = 0
    # FN = 0
    # P = 0
    # N = 0
    ytestPre = bdt.predict(testArr)
    # result = (y_test == ytestPre)
    # accuracy = np.mean(result)
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(testLabelArr, ytestPre)
    print(u'准确率： %.4f%%' % (100 * accuracy))
    from sklearn import metrics
    precision = metrics.precision_score(testLabelArr, ytestPre, average='micro')  # 微平均，精确率
    print(u'微平均，精确率： %.4f%%' % (100 * precision))
    recall = metrics.recall_score(testLabelArr, ytestPre, average='macro')
    print(u'微平均，召回率： %.4f%%' % (100 * recall))
    f1_score = metrics.f1_score(testLabelArr, ytestPre, average='weighted')
    print(u'微平均，调和平均数： %.4f%%' % (100 * f1_score))
    from sklearn.metrics import classification_report
    # target_names = ['label is 1', 'label is 2']
    print(classification_report(testLabelArr, ytestPre, target_names=target_names))
    from sklearn.metrics import cohen_kappa_score
    kappa_score = cohen_kappa_score(testLabelArr, ytestPre)
    print(u'kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： %.4f%%' % (100 * kappa_score))
    # pre_result = bdt.predict_log_proba(testLabelArr)
    # ROC_AUC(testLabelArr, pre_result)
    # from sklearn.tree import export_graphviz
    # dot_data = export_graphviz(bdt, out_file=None,  # doctest: +SKIP
    #                                 feature_names=feature_names,  # doctest: +SKIP
    #                                 class_names=target_names,  # doctest: +SKIP
    #                                 filled=True, rounded=True,  # doctest: +SKIP
    #                                 special_characters=True)
    # graph = graphviz.Source(dot_data)  # doctest: +SKIP
    # graph.render("./sklearn_result01/dx_adaboost_fig01")


def xgboost_train():
    target_names = ['label is 2', 'label is 1']
    import xgboost as xgb
    dataMat, labelMat = loadDataSet(filepath2)
    dataMat = np.array(dataMat)
    labelMat = np.array(labelMat)
    labelMat = np.where(labelMat <2, labelMat, 0)
    X_train, X_test, y_train, y_test = dealdata(dataMat, labelMat)
    max_depth = 10
    subsample = 0.95
    num_round = 2000
    early_stopping_rounds = 50
    params = {'max_depth': max_depth, 'eta': 0.1, 'silent': 1, 'alpha': 0.5, 'lambda': 0.5,
                   'eval_metric': 'auc', 'subsample': subsample, 'objective': 'binary:logistic'}
    num_round = num_round
    early_stopping_rounds = early_stopping_rounds
    clf = xgb.XGBClassifier(learning_rate = 0.1,
    n_estimators =30,
    max_depth =40,
    min_child_weight = 1,
    gamma = 0.15,
    subsample = 0.8,
    colsample_bytree = 0.8,
    nthread = 4,
    scale_pos_weight = 1,
    seed = 27)
    clf.fit(X_train, y_train, early_stopping_rounds=10, eval_metric="auc",
            eval_set=[(X_test, y_test)])

    # dtrain = xgb.DMatrix(X_train)
    # deval = xgb.DMatrix(y_train)
    # clf = xgb.train(params, dtrain, num_boost_round=num_round,
    #                         evals=[(dtrain, 'train'), (deval, 'eval')],
    #                         early_stopping_rounds=early_stopping_rounds, verbose_eval=False)
    # print('get best eval auc : %s, in step %s' % (clf.best_score, clf.best_iteration))
    ytestPre = clf.predict(X_test)
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(y_test, ytestPre)
    print(u'准确率： %.4f%%' % (100 * accuracy))
    from sklearn import metrics
    precision = metrics.precision_score(y_test, ytestPre, average='micro')  # 微平均，精确率
    print(u'微平均，精确率： %.4f%%' % (100 * precision))
    recall = metrics.recall_score(y_test, ytestPre, average='macro')
    print(u'微平均，召回率： %.4f%%' % (100 * recall))
    f1_score = metrics.f1_score(y_test, ytestPre, average='weighted')
    print(u'微平均，调和平均数： %.4f%%' % (100 * f1_score))
    from sklearn.metrics import classification_report
    print(classification_report(y_test, ytestPre, target_names=target_names))
    from sklearn.metrics import cohen_kappa_score
    kappa_score = cohen_kappa_score(y_test, ytestPre)
    print(u'kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： %.4f%%' % (100 * kappa_score))
    pre_result = clf.predict_proba(X_test)

    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve
    fpr, tpr, thresholds = roc_curve(y_test, pre_result[:, 1], pos_label=1)
    from sklearn.metrics import auc
    auc_area = auc(fpr, tpr)
    # 画图，只需要plt.plot(fpr,tpr),变量roc_auc只是记录auc的值，通过auc()函数能计算出来
    plt.plot(fpr, tpr, lw=1, label='ROC  (area = %0.2f)' % (auc_area))
    print("auc_area:" + str(auc_area))
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()


def lightgbm_train():
    target_names = ['label is 2', 'label is 1']
    import xgboost as xgb
    dataMat = np.loadtxt("dataMat_train.txt", delimiter=',')
    labelMat = np.loadtxt("data_labelMat_train.txt", delimiter=',')
    labelMat = np.where(labelMat <2, labelMat, 0)
    X_train, X_test, y_train, y_test = dealdata(dataMat, labelMat)
    max_depth = 3
    subsample = 0.95
    num_round = 2000
    early_stopping_rounds = 50
    params = {'max_depth': max_depth, 'eta': 0.1, 'silent': 1, 'alpha': 0.5, 'lambda': 0.5,
                   'eval_metric': 'auc', 'subsample': subsample, 'objective': 'binary:logistic'}
    num_round = num_round
    early_stopping_rounds = early_stopping_rounds
    import lightgbm
    clf = lightgbm.LGBMClassifier(boosting_type='gbdt', num_leaves=2 ** 3, objective='binary',
                                  max_depth=8, learning_rate=0.1, n_estimators=100,
                                  metric="auc",
                                  reg_alpha=0.1,
                                  )
    clf.fit(X_train, y_train, early_stopping_rounds=10, eval_metric="auc",
            eval_set=[(X_test, y_test)])

    # dtrain = xgb.DMatrix(X_train)
    # deval = xgb.DMatrix(y_train)
    # clf = xgb.train(params, dtrain, num_boost_round=num_round,
    #                         evals=[(dtrain, 'train'), (deval, 'eval')],
    #                         early_stopping_rounds=early_stopping_rounds, verbose_eval=False)
    # print('get best eval auc : %s, in step %s' % (clf.best_score, clf.best_iteration))
    ytestPre = clf.predict(X_test)
    from sklearn.metrics import accuracy_score
    accuracy = accuracy_score(y_test, ytestPre)
    print(u'准确率： %.4f%%' % (100 * accuracy))
    from sklearn import metrics
    precision = metrics.precision_score(y_test, ytestPre, average='micro')  # 微平均，精确率
    print(u'微平均，精确率： %.4f%%' % (100 * precision))
    recall = metrics.recall_score(y_test, ytestPre, average='macro')
    print(u'微平均，召回率： %.4f%%' % (100 * recall))
    f1_score = metrics.f1_score(y_test, ytestPre, average='weighted')
    print(u'微平均，调和平均数： %.4f%%' % (100 * f1_score))
    from sklearn.metrics import classification_report
    print(classification_report(y_test, ytestPre, target_names=target_names))
    from sklearn.metrics import cohen_kappa_score
    kappa_score = cohen_kappa_score(y_test, ytestPre)
    print(u'kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： %.4f%%' % (100 * kappa_score))
    pre_result = clf.predict_proba(X_test)

    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve
    fpr, tpr, thresholds = roc_curve(y_test, pre_result[:, 1], pos_label=1)
    from sklearn.metrics import auc
    auc_area = auc(fpr, tpr)
    # 画图，只需要plt.plot(fpr,tpr),变量roc_auc只是记录auc的值，通过auc()函数能计算出来
    plt.plot(fpr, tpr, lw=1, label='ROC  (area = %0.2f)' % (auc_area))
    print("auc_area:" + str(auc_area))
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()


if __name__ == '__main__':
    # test03()
    # dx_train()
    # dx_train2()
    sklearn_single_classficatopn_test()
    # AdaBoost_dx_train()
    # feature_importance()