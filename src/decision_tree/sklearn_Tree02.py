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

filepath = "ljt_train_dx.txt"

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
    if sum >= 1:
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

def dx_train():
    from sklearn import tree
    data, target = loadDataSet()
    X_train, X_test, y_train, y_test = dealdata(data, target)
    clf = tree.DecisionTreeClassifier()

    clf = clf.fit(X_train, y_train)
    print clf.feature_importances_
    # from sklearn.externals import joblib
    # #保存模型
    # joblib.dump(clf, "./sklearn_result01/dx_train_model.m", compress=3)
    # clf = joblib.load("./sklearn_result01/dx_train_model.m")
    # import graphviz

    # dxFeature = ["judgedoc_is_no", "judgedoc_cnt", "litigant_defendant_cnt", "near_3_year_judgedoc_cnt",
    #              "near_2_year_judgedoc_cnt", "near_1_year_judgedoc_cnt", "litigant_defendant_contract_dispute_cnt",
    #              "litigant_defendant_bust_cnt", "litigant_defendant_infringe_cnt",
    #              "litigant_defendant_Intellectual_property_owner_cnt", "litigant_defendant_unjust_enrich_cnt",
    #              "litigant_result_sum_money", "net_judgedoc_defendant_cnt",
    #              "shixin_is_no", "shixin_cnt", "near_3_year_shixin_cnt", "near_2_year_shixin_cnt",
    #              "near_1_year_shixin_cnt", "court_announce_is_no",
    #              "court_announce_cnt", "court_announce_litigant_cnt", "court_notice_is_no", "court_notice_cnt",
    #              "court_notice_litigant_cnt"]
    # feature_names = np.array(dxFeature)
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
    # print("---------------------------------------------------------------")
    # sizePre = len(ytestPre)
    # for i in range(sizePre):
    #     y = y_test[i]
    #     if y == 0:
    #         # 正样本
    #         P += 1
    #     else:
    #         N += 1
    #     pre01 = ytestPre[i]
    #     if pre01 == y and pre01 == 0: # TP，真正
    #         TP += 1
    #     elif pre01 == y and pre01 == 0: # TN，真负
    #         TN += 1
    #     elif pre01 != y and pre01 == 1: # FN， 假负
    #         FN += 1
    #     elif pre01 != y and pre01 == 0: # FP， 假正
    #         FP += 1
    # recall = Recall(P, TP)
    # print("召回率："+str(recall))
    # precision = Precision(TP, FN)
    # print("精度："+str(precision))
    # print("调和平均数：" + str(2.0/((1.0/precision)+(1.0/recall))))

    # dot_data = tree.export_graphviz(clf, out_file=None,  # doctest: +SKIP
    #                                      feature_names=feature_names,  # doctest: +SKIP
    #                                      class_names=target_names,  # doctest: +SKIP
    #                                      filled=True, rounded=True,  # doctest: +SKIP
    #                                      special_characters=True)  # doctest: +SKIP
    # graph = graphviz.Source(dot_data)  # doctest: +SKIP
    # graph.render("./sklearn_result01/dx_fig01")



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