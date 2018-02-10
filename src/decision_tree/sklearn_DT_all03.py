# -*- coding: utf-8 -*-
'''
Created on  : 20180208
@author: ljt
决策树：
'''
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

filepath = "ljt_train_dx.txt"
dxFeature = ["judgedoc_is_no", "judgedoc_cnt", "litigant_defendant_cnt",
"near_3_year_judgedoc_cnt", "near_2_year_judgedoc_cnt",
"near_1_year_judgedoc_cnt", "litigant_defendant_contract_dispute_cnt",
  "litigant_defendant_bust_cnt",  "litigant_defendant_infringe_cnt",
  "litigant_defendant_intellectual_property_owner_cnt",
  "litigant_defendant_unjust_enrich_cnt",
  "litigant_result_sum_money",  "net_judgedoc_defendant_cnt", "shixin_is_no",
  "shixin_cnt", "near_3_year_shixin_cnt", "near_2_year_shixin_cnt",
  "near_1_year_shixin_cnt", "court_announce_is_no", "court_announce_cnt",
  "court_announce_litigant_cnt",  "court_notice_is_no", "court_notice_cnt",
  "court_notice_litigant_cnt",  "industry", "province", "regcap", "zczjbz",
  "established_years",  "fr_change_cnt",  "address_change_cnt", "regcap_change_cnt",
  "share_change_cnt", "network_fr_share_change_cnt",  "network_share_shixin_cnt",
  "zhixing_cnt",  "sszc_cnt", "punish_cnt", "judge_doc_cnt",  "cancel_cnt",
  "bidding_cnt",  "bidding_three_year_rate",  "is_black_list",  "is_escape",
  "is_diff_raise_money",  "is_stop_busi", "is_lost_with_money", "is_just_lost",
  "invent_publish_cnt", "invent_patent_cnt",  "utility_publish_cnt",
  "invent_publish_three_year_rate", "invent_patent_three_year_rate",
  "utility_publish_three_year_rate",  "warn_cnt", "fine_cnt", "revoking_cnt",
  "warn_cnt_three_year_rate", "fine_cnt_three_year_rate", "revoking_cnt_three_year_rate",
  "estate_auction_cnt", "real_estate_auction_cnt",  "trade_mark_cnt",
  "trademark_three_year_rate"]

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
                itrm = 0.0
            else:
                itrm = float(itrm)
                itrm = abs(itrm)
                if itrm >= 0:
                    import math
                    itrm = math.log(itrm+1)
            sum += itrm
    if sum >= 2:
        return False
    else:
        return True

def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open(filepath)
    count = 0.0
    count01 = 0.0
    for line in fr.readlines():
        curLine = line.strip().split(',')
        if is_empty_data_delet(curLine):
            continue
        lineArr = []
        # 调整正负样本比例
        label = float(curLine[-1])
        size = len(curLine)
        # for i in range(size - 1):
        #     lineArr.append(float(curLine[i]))
        # dataMat.append(lineArr)
        # labelMat.append(label)
        if label == 1.0:
            for i in range(size-1):
                lineArr.append(float(curLine[i]))
            dataMat.append(lineArr)
            labelMat.append(label)
            count += 1
        if label == 0.0:
            if count01 >= count:
                continue
            for i in range(size - 1):
                lineArr.append(float(curLine[i]))
            labelMat.append(label)
            dataMat.append(lineArr)
            count01 += 1

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
        print("%d. %s: %d (%f)" % (f + 1,dxFeature[f], indices[f], importances[indices[f]]))

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
    clf = ExtraTreesClassifier(criterion="entropy", n_estimators=250,
                                  random_state=0)
    # from sklearn.ensemble import RandomForestClassifier
    # clf = RandomForestClassifier(criterion="entropy", n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
    '''
    决策树
    '''
    # clf = tree.DecisionTreeClassifier(max_depth=24, splitter="best", criterion='entropy',
    #                                   max_features=24, min_samples_split=24,
    #                                   max_leaf_nodes=24)

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
    size = 25
    # Print the feature ranking
    print("Feature ranking:")
    for f in range(size - 1):
        print("%d. %s: %d (%f)" % (f + 1, dxFeature[f], indices[f], importances[indices[f]]))

    # from sklearn.externals import joblib
    # #保存模型
    # joblib.dump(clf, "./sklearn_result01/dx_train_model.m", compress=3)
    # clf = joblib.load("./sklearn_result01/dx_train_model.m")
    import graphviz

    # dxFeature = ["judgedoc_is_no", "judgedoc_cnt", "litigant_defendant_cnt", "near_3_year_judgedoc_cnt",
    #              "near_2_year_judgedoc_cnt", "near_1_year_judgedoc_cnt", "litigant_defendant_contract_dispute_cnt",
    #              "litigant_defendant_bust_cnt", "litigant_defendant_infringe_cnt",
    #              "litigant_defendant_Intellectual_property_owner_cnt", "litigant_defendant_unjust_enrich_cnt",
    #              "litigant_result_sum_money", "net_judgedoc_defendant_cnt",
    #              "shixin_is_no", "shixin_cnt", "near_3_year_shixin_cnt", "near_2_year_shixin_cnt",
    #              "near_1_year_shixin_cnt", "court_announce_is_no",
    #              "court_announce_cnt", "court_announce_litigant_cnt", "court_notice_is_no", "court_notice_cnt",
    #              "court_notice_litigant_cnt"]
    feature_names = np.array(dxFeature)
    # TP = 0
    # FP = 0
    # TN = 0
    # FN = 0
    # P = 0
    # N = 0
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
    target_names = ['label is 0', 'label is 1']
    print(classification_report(y_test, ytestPre, target_names=target_names))
    from sklearn.metrics import cohen_kappa_score
    kappa_score = cohen_kappa_score(y_test, ytestPre)
    print(u'kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： %.4f%%' % (100 * kappa_score))
    pre_result = clf.predict_proba(X_test)
    ROC_AUC(y_test, pre_result)
    dot_data = tree.export_graphviz(clf, out_file=None,  # doctest: +SKIP
                                         feature_names=feature_names,  # doctest: +SKIP
                                         class_names=target_names,  # doctest: +SKIP
                                         filled=True, rounded=True,  # doctest: +SKIP
                                         special_characters=True)
    graph = graphviz.Source(dot_data)  # doctest: +SKIP
    graph.render("./sklearn_result01/dx_fig01")
    # from sklearn.tree import export_graphviz
    # for i in xrange(len(clf.estimators_)):
    #     # export_graphviz(clf.estimators_[i], '%d.dot' % i)
    #     dot_data = export_graphviz(clf.estimators_[i], out_file=None,  # doctest: +SKIP
    #                                          feature_names=feature_names,  # doctest: +SKIP
    #                                          class_names=target_names,  # doctest: +SKIP
    #                                          filled=True, rounded=True,  # doctest: +SKIP
    #                                          special_characters=True)  # doctest: +SKIP
    #     graph = graphviz.Source(dot_data)  # doctest: +SKIP
    #     graph.render("./sklearn_result01/dx_fig01"+str(i))





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
    size = 25
    # Print the feature ranking
    print("Feature ranking:")
    for f in range(size - 1):
        print("%d. %s: %d (%f)" % (f + 1, dxFeature[f], indices[f], importances[indices[f]]))

    # from sklearn.externals import joblib
    # #保存模型
    # joblib.dump(clf, "./sklearn_result01/dx_train_model.m", compress=3)
    # clf = joblib.load("./sklearn_result01/dx_train_model.m")
    import graphviz
    feature_names = np.array(dxFeature)
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
    target_names = ['label is 0', 'label is 1']
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

if __name__ == '__main__':
    # test03()
    # dx_train()
    AdaBoost_dx_train()
    # feature_importance()