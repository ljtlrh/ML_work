# -*- coding: utf-8 -*-
'''
Created on  : 20180208
@author: ljt
决策树：
'''
import json

import numpy as np
import pandas as pd
from sklearn import tree
import matplotlib.pyplot as plt

class DecisionTreeClassifierParser(object):
	'''
	对决策树进行解析
	'''

	def __init__(self, model, feature_names):
		'''
		:param model: 已训练完成的决策树模型
		:param feature_names: list类型，训练数据的特征名字，按训练时的顺序排列
		:return:
		'''
		self.model = model
		self.feature_names = feature_names
		# 仅支持DecisionTreeClassifier模型
		if not isinstance(self.model, tree.DecisionTreeClassifier):
			raise ('The given model is not the supported sklearn model DecisionTreeClassifier')

	def __parser(self):
		'''
		递归算法解析决策树的每个分支
		参考部分代码：　https://stackoverflow.com/questions/20224526/how-to-extract-the-decision-rules-from-scikit-learn-decision-tree
		:return:
		'''
		parsed_tree = []
		# 左节点id
		left = self.model.tree_.children_left
		# 右节点id
		right = self.model.tree_.children_right
		# 节点阈值
		threshold = self.model.tree_.threshold
		# 特征名字
		features = [self.feature_names[i] for i in self.model.tree_.feature]
		# value 是该节点上不同标签样本的数量
		values = self.model.tree_.value
		# 该节点sample的总数量，理论上value的和即为sample的总数
		number_of_nodes = self.model.tree_.weighted_n_node_samples
		# 节点不纯度
		# impurity = tree.tree_.impurity
		# 叶子节点id列表
		idx = np.argwhere(left == -1)[:, 0]

		def recurse(left, right, child, lineage=None):
			if lineage is None:
				v = values[child][0]
				label = np.argmax(v)
				# 该节点误分率
				missclassfication_rate = min(v) / sum(v)
				# node_impurity = impurity[child]
				# 终节点id, 标签，训练集中归于该节点的数量，错分概率
				lineage = [(child, 'leaf', label, int(number_of_nodes[child]), missclassfication_rate)]
			if child in left:
				parent = np.where(left == child)[0].item()
				split = '<='
			else:
				parent = np.where(right == child)[0].item()
				split = '>'

			lineage.append((parent, split, threshold[parent], features[parent]))

			if parent == 0:
				lineage.reverse()
				return lineage
			else:
				return recurse(left, right, parent, lineage)

		for child in idx:
			one_branch = []
			for node in recurse(left, right, child):
				one_branch.append(node)
			parsed_tree.append(one_branch)
		return parsed_tree

	def get_parsed_tree(self):
		'''输出决策树的解析结果.
		Returns
		-------
		[
		  {
			"missclassfication_rate": 0.5, #改路径错误分类率
			"sample_number": 2,　#该路径样本数据量
			"statement": "col2 <= 5.5 and col1 <= 1.5 and col2 <= 3.5",　#该路径的条件组合, 并且作冗余的归并，例如col2 > 3.5 and col2 > 4.5归并为col2 > 4.5
			"label": 0　#该路径的样本被预测的标签
		  }
		]
		'''
		res = []
		for t in self.__parser():
			sub_statement = []
			sub_statement_container = {}  # 以col1 <=作为key
			for each in t[0:-1]:
				# 可互相包含的决策路径逻辑合并处理
				statement_key = str(each[3]) + ' ' + str(each[1])
				if statement_key in sub_statement_container.keys():
					if each[1] == '>' and sub_statement_container[statement_key] < each[2]:
						sub_statement.remove(statement_key + ' ' + str(sub_statement_container[statement_key]))
						sub_statement.append(statement_key + ' ' + str(each[2]))
						sub_statement_container[statement_key] = each[2]
					elif each[1] == '<=' and sub_statement_container[statement_key] > each[2]:
						sub_statement.remove(statement_key + ' ' + str(sub_statement_container[statement_key]))
						sub_statement.append(statement_key + ' ' + str(each[2]))
						sub_statement_container[statement_key] = each[2]
				else:
					sub_statement_container[statement_key] = each[2]
					sub_statement.append(str(each[3]) + ' ' + str(each[1]) + ' ' + str(each[2]))
			res.append({
				'decision_path': ' and '.join(sub_statement),  # 以and的形式组合
				'label': t[-1][2],
				'sample_number': t[-1][3],
				'missclassfication_rate': t[-1][4]
			})

		return res

target_names = ['label is 1', 'label is 2']
file_path = "/home/sinly/ljtstudy/back/0315/update_trade_cnt_feature_data.csv"
filepath2 = "data_dx2_zc03.txt"
feature_name = ["established_years", "industry_dx_rate", "regcap_change_cnt", "industry_all_cnt", "share_change_cnt",
             "address_change_cnt", "industry_dx_cnt", "cancel_cnt", "network_share_cancel_cnt", "fr_change_cnt",
             "trade_mark_cnt",
             "bidding_cnt", "judgedoc_cnt", "network_share_zhixing_cnt", "judge_doc_cnt", "net_judgedoc_defendant_cnt",
             "network_share_judge_doc_cnt"]


def isNone(d):
    from operator import eq as cmp
    return (d is None or d == 'None' or
            d == '?' or
            d == '' or
            d == 'NULL' or
            d == 'null')


filter_cnt = 0.0


def is_empty_data_delet(curLine, label):
    global filter_cnt
    sum = 0.0
    court = 0.0
    lineArr = []
    if isinstance(curLine, list):
        size = len(curLine)
        for i in range(size - 1):
            itrm = curLine[i + 1]
            if isNone(itrm):
                itrm = 0.0
            else:
                try:
                    itrm = float(itrm)
                    if itrm > 0 and i != 12 and i != 31 and i != 32 and i != 33:
                        court += itrm
                    lineArr.append(itrm)
                except:
                    continue
    import math
    sum = math.log(court + 1)
    if label == 2.0:  # 负样本，吊销企业,事件发生较少
        if sum <= 1.2:
            lineArr = []
            filter_cnt += 1
            print ("sum:" + str(sum) + "===>label: " + str(label) + " vector:" + str(curLine))
            return lineArr
    elif label == 1.0:  # 正样本，正常企业,事件发生较多
        if sum >= 9:
            # filter_cnt += 1
            print ("sum:" + str(sum) + "===>label:" + str(label) + " vector:" + str(curLine))
            lineArr = []
            return lineArr
    return lineArr


def loadDataSet(filepath00):
    dataMat = []
    labelMat = []
    fr = open(filepath00)
    count = 0.0
    count01 = 0.0
    for line in fr.readlines():
        curLine = line.strip().split(',')
        # 调整正负样本比例
        size = len(curLine)
        if size < 64:
            continue
        label = float(curLine[0])
        # for i in range(size - 1):
        #     lineArr.append(float(curLine[i]))
        # dataMat.append(lineArr)
        # labelMat.append(label)
        if label == 2.0:  # 负样本，吊销企业
            if count >= 116524:
                continue
            lineArr = is_empty_data_delet(curLine, label)
            if len(lineArr) < 60:
                continue
            dataMat.append(lineArr)
            labelMat.append(label)
            count += 1
            # print (count)
        if label == 1.0:  # 正样本，正常企业
            if count01 > 116524:
                continue
            lineArr = is_empty_data_delet(curLine, label)
            if len(lineArr) < 60:
                continue
            labelMat.append(label)
            dataMat.append(lineArr)
            count01 += 1
            # print (count01)
    try:
        print ("start")
        # np.savetxt("dataMat_train.txt", dataMat, delimiter=',')
        # np.savetxt("data_labelMat_train.txt", labelMat)
        # dataMat = np.loadtxt("dataMat_train.txt", delimiter=',')
        # dataMat = dataMat.tolist()
        # labelMat = np.loadtxt("data_labelMat_train.txt", delimiter=',')
        # labelMat = labelMat.tolist()
    except:
        print ("fffff")
    print ("filter company num:" + str(filter_cnt))
    print ("data len : " + str(len(dataMat)))
    return dataMat, labelMat


def random_read_txt(dataMat, labelMat, file01, num01):
    import random
    count01 = 0
    with open(file01, 'r') as f:
        lines = f.readlines()
        flen = len(lines) - 1
        if num01 <= flen:
            for line in f.readlines():
                curLine = line.strip().split(',')
                if is_empty_data_delet(curLine):
                    continue
                lineArr = []
                # 调整正负样本比例
                label = float(curLine[-1])
                size = len(curLine)
                for i in range(size - 1):
                    lineArr.append(float(curLine[i]))
                dataMat.append(lineArr)
                labelMat.append(label)
                count01 += 1
                if count01 >= num01:
                    break
        elif num01 <= flen:
            for i in range(1, flen):
                line = lines[random.randint(0, flen)]
                curLine = line.strip().split(',')
                if is_empty_data_delet(curLine):
                    continue
                lineArr = []
                # 调整正负样本比例
                # write_txt(random_zc_txt, curLine)
                label = float(curLine[0])
                size = len(curLine)
                for i in range(size - 1):
                    try:
                        item = float(curLine[i + 1])
                    except:
                        item = str(item)
                    lineArr.append(item)
                dataMat.append(lineArr)
                labelMat.append(label)
                count01 += 1
                if count01 >= num01:
                    break
    return dataMat, labelMat


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


def Recall(P, TP):
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
    return TP / (TP * 1.0 + FP * 1.0)


def TP_RATE(P, TP):
    '''
    正确率：原本是对的预测为对的比率
    :param P:  正样本
    :param TP: 真正，被模型预测为正的正样本
    :return:
    '''
    return TP / (P * 1.0)


def FP_RATE(N, FP):
    '''
    错误率：原本是错的预测为对的比率
    :param N:  负样本
    :param FP: 假正，被模型预测为正的负样本
    :return:
    '''
    return FP / (N * 1.0)


def ROC_AUC(y, pred):
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve
    # y = np.array([1, 1, 2, 2])
    # pred = np.array([0.1, 0.4, 0.35, 0.8])
    fpr, tpr, thresholds = roc_curve(y, pred[:, 1], pos_label=1)
    # print("正确率：fpr==>"+str(fpr))
    # print("错误率：tpr==>"+str(tpr))
    # print(thresholds)
    from sklearn.metrics import auc
    auc_area = auc(fpr, tpr)
    # 画图，只需要plt.plot(fpr,tpr),变量roc_auc只是记录auc的值，通过auc()函数能计算出来
    plt.plot(fpr, tpr, lw=1, label='ROC  (area = %0.2f)' % (auc_area))
    print("auc_area:" + str(auc_area))
    # plt.xlim([-0.05, 1.05])
    # plt.ylim([-0.05, 1.05])
    # plt.xlabel('False Positive Rate')
    # plt.ylabel('True Positive Rate')
    # plt.title('Receiver operating characteristic example')
    # plt.legend(loc="lower right")
    # plt.savefig("./sklearn_result01/aoc_fig.png")
    # plt.show()


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

    for f in range(size - 1):
        print("%d. %s: %d (%f)" % (f + 1, feature_name[f], indices[f], importances[indices[f]]))

    # Plot the feature importances of the forest
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(size - 1), importances[indices],
            color="r", yerr=std[indices], align="center")
    plt.xticks(range(size - 1), indices)
    plt.xlim([-1, size - 1])
    plt.show()


def dx_train():
    df = pd.read_csv(file_path)
    df_p = df[df['_c1'] == 1].head(389081)
    df_n = df[df['_c1'] == 2].head(389081)
    frames = [df_p, df_n]
    df = pd.concat(frames)
    df = df.fillna(0)
    # df = pd.to_numeric(df, errors='coerce')
    target = df['_c1'].as_matrix()
    target = pd.to_numeric(target, errors='coerce')
    data = df[feature_name].astype(float).as_matrix()
    X_train, X_test, y_train, y_test = dealdata(data, target)
    # from sklearn.ensemble import ExtraTreesClassifier
    '''
    附加树分类器。
这个类实现了一个元估计适合许多随机决策树（又名多余的树木）的数据集，使用平均提高了拟合预测的精度和控制各子样本。
    '''
    # clf = ExtraTreesClassifier(n_estimators=130,
    #                               random_state=0)
    # from sklearn.ensemble import RandomForestClassifier
    # clf = RandomForestClassifier(criterion="entropy", n_estimators=10, max_depth=None, min_samples_split=2, random_state=0)
    '''
    决策树
    '''
    clf = tree.DecisionTreeClassifier(max_depth=7, splitter="best",
                                      max_features=17, min_samples_split=17,
                                      max_leaf_nodes=100)


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
    size = len(feature_name)
    # Print the feature ranking
    print(str(size) + " Feature ranking:")
    for f in range(size):
        print("feature name: %s <==> importances rate: (%f)" % (feature_name[indices[f]], importances[indices[f]]))

    # from sklearn.externals import joblib
    # #保存模型
    # joblib.dump(clf, "./sklearn_result01/dx_train_model.m", compress=3)
    # clf = joblib.load("./sklearn_result01/dx_train_model.m")
    import graphviz

    # feature_name = ["judgedoc_is_no", "judgedoc_cnt", "litigant_defendant_cnt", "near_3_year_judgedoc_cnt",
    #              "near_2_year_judgedoc_cnt", "near_1_year_judgedoc_cnt", "litigant_defendant_contract_dispute_cnt",
    #              "litigant_defendant_bust_cnt", "litigant_defendant_infringe_cnt",
    #              "litigant_defendant_Intellectual_property_owner_cnt", "litigant_defendant_unjust_enrich_cnt",
    #              "litigant_result_sum_money", "net_judgedoc_defendant_cnt",
    #              "shixin_is_no", "shixin_cnt", "near_3_year_shixin_cnt", "near_2_year_shixin_cnt",
    #              "near_1_year_shixin_cnt", "court_announce_is_no",
    #              "court_announce_cnt", "court_announce_litigant_cnt", "court_notice_is_no", "court_notice_cnt",
    #              "court_notice_litigant_cnt"]
    feature_names = np.array(feature_name)
    # TP = 0
    # FP = 0
    # TN = 0
    # FN = 0
    # P = 0
    # N = 0
    ytestPre = clf.predict(X_test)
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
    target_names = ['label is 1', 'label is 2']
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
    dtp = DecisionTreeClassifierParser(clf, feature_name)
    res = dtp.get_parsed_tree()
    print json.dumps(res, ensure_ascii=False, indent=2)


def evaluate_function(clf, X_test, y_test):
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


def plot_fig(clf, figpath):
    import graphviz
    feature_names = np.array(feature_name)
    dot_data = tree.export_graphviz(clf, out_file=None,  # doctest: +SKIP
                                    feature_names=feature_names,  # doctest: +SKIP
                                    class_names=target_names,  # doctest: +SKIP
                                    filled=True, rounded=True,  # doctest: +SKIP
                                    special_characters=True)
    graph = graphviz.Source(dot_data)  # doctest: +SKIP
    graph.render(figpath)


def dx_train2():
    from sklearn import ensemble
    data, target = loadDataSet(filepath2)

    X_train, X_test, y_train, y_test = dealdata(data, target)
    from sklearn.ensemble import ExtraTreesClassifier
    '''
    附加树分类器。
    这个类实现了一个元估计适合许多随机决策树（又名多余的树木）的数据集，使用平均提高了拟合预测的精度和控制各子样本。
    '''
    clf = ExtraTreesClassifier(n_estimators=250,
                               random_state=0, max_depth=60)
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
    size = len(feature_name)
    # Print the feature ranking
    print(str(size) + " criterion='gini', Feature ranking:")
    for f in range(size):
        print("feature name: %s <==> importances rate: (%f)" % (feature_name[indices[f]], importances[indices[f]]))

    # from sklearn.externals import joblib
    # #保存模型
    # joblib.dump(clf, "./sklearn_result01/dx_train_model.m", compress=3)
    # clf = joblib.load("./sklearn_result01/dx_train_model.m")
    evaluate_function(clf, X_test, y_test)
    # plot_fig(clf, "./sklearn_result01/dx_fig01")


def sklearn_single_classficatopn_test():
    '''
     sklearn 大致可以将这些分类器分成两类：
     1）单一分类器
     2）集成分类器
    :return:
    '''
    data, target = loadDataSet(filepath2)
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
        # 'KNeighborsClassifier': KNeighborsClassifier(3),
        # 'SVC_linear': SVC(kernel="linear", C=0.025),
        # 'SVC': SVC(gamma=2, C=1),
        'DecisionTreeClassifier': DecisionTreeClassifier(max_depth=60, splitter="best",
                                                         max_features=60, min_samples_split=60,
                                                         max_leaf_nodes=124),
        'RandomForestClassifier': RandomForestClassifier(n_estimators=60, max_depth=65, max_features=65),
    # clf.feature_importances_
        'ExtraTreesClassifier': ExtraTreesClassifier(n_estimators=120, max_depth=65),  # clf.feature_importances_
        'AdaBoostClassifier': AdaBoostClassifier(DecisionTreeClassifier(max_depth=62), algorithm="SAMME",
                                                 n_estimators=120),
        'GradientBoostingClassifier': GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1,
                                                                 random_state=0),
        'GaussianNB': GaussianNB(),
        'LinearDiscriminantAnalysis': LinearDiscriminantAnalysis(),
        'QuadraticDiscriminantAnalysis': QuadraticDiscriminantAnalysis()}

    for name, clf in classifiers.items():
        print (name)
        clf = clf.fit(X_train, y_train)
        # importances = clf.feature_importances_
        # indices = np.argsort(importances)[::-1]
        # size = len(feature_name)
        # Print the feature ranking
        # print(str(size)+" criterion='gini', Feature ranking:")
        # for f in range(size):
        #     print("feature name: %s <==> importances rate: (%f)" % (feature_name[indices[f]], importances[indices[f]]))

        # from sklearn.externals import joblib
        # #保存模型
        # joblib.dump(clf, "./sklearn_result01/dx_train_model.m", compress=3)
        # clf = joblib.load("./sklearn_result01/dx_train_model.m")
        evaluate_function(clf, X_test, y_test)
        # plot_fig("./sklearn_result01/dx_fig01")


def Bagging_train():
    '''
    一般会随机采集和训练集样本数m一样个数的样本。这样得到的采样集和训练集样本的个数相同，
    但是样本内容不同。如果我们对有m个样本训练集做T次的随机采样，则由于随机性，T个采样集各不相同。
    :return:
    '''
    from sklearn.ensemble import BaggingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    data, target = loadDataSet(filepath2)
    X_train, X_test, y_train, y_test = dealdata(data, target)
    meta_clf = KNeighborsClassifier()
    bg_clf = BaggingClassifier(meta_clf, max_samples=0.5, max_features=0.5)
    return bg_clf


def voting_train():
    '''
    投票决策
    :return:
    '''
    from sklearn import model_selection
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import GaussianNB
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.ensemble import VotingClassifier
    data, target = loadDataSet(filepath2)
    X_train, X_test, y_train, y_test = dealdata(data, target)

    clf1 = LogisticRegression(random_state=1)
    clf2 = RandomForestClassifier(random_state=1)
    clf3 = GaussianNB()

    eclf = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='hard', weights=[2, 1, 2])

    for clf, label in zip([clf1, clf2, clf3, eclf],
                          ['Logistic Regression', 'Random Forest', 'naive Bayes', 'Ensemble']):
        scores = model_selection.cross_val_score(clf, X_train, y_train, cv=5, scoring='accuracy')
        print("Accuracy: %0.2f (+/- %0.2f) [%s]" % (scores.mean(), scores.std(), label))
        # evaluate_function(clf, X_test, y_test)


def GridSearch_train():
    import time
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import GridSearchCV
    from sklearn.model_selection import RandomizedSearchCV

    # 生成数据
    iris = load_iris()
    # data, target = loadDataSet(filepath2)
    data = np.loadtxt("dataMat_train.txt", delimiter=',')
    target = np.loadtxt("data_labelMat_train.txt", delimiter=',')
    X_train, X_test, y_train, y_test = dealdata(data, target)
    # 设置参数
    # parameter_space = {"max_depth": [3, 64],
    #               "max_features":  [10, 15, 20],
    #               "min_samples_leaf": [2, 4, 6],
    #               "bootstrap": [True, False],
    #               "criterion": ["gini", "entropy"]}
    parameter_space = {
        "n_estimators": [10, 15, 18],
        "criterion": ["gini", "entropy"],
        "min_samples_leaf": [2, 4, 6],
    }

    # 运行随机搜索 RandomizedSearch
    n_iter_search = 10

    # scores = ['precision', 'recall', 'roc_auc']
    scores = ['roc_auc']

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        # 元分类器
        clf = RandomForestClassifier(random_state=60)
        rs_clf = RandomizedSearchCV(clf, param_distributions=parameter_space,
                                    n_iter=n_iter_search)

        start = time.time()
        rs_clf.fit(X_train, y_train)
        evaluate_function(rs_clf, X_test, y_test)
        print ("cost time:" + str(time.time() - start))


def ensemble_train():
    '''
     sklearn 大致可以将这些分类器分成两类：
     2）集成分类器
     集成分类器有四种：Bagging, Voting, GridSearch, PipeLine。
     最后一个PipeLine其实是管道技术
    :return:
    '''
    data, target = loadDataSet(filepath2)
    X_train, X_test, y_train, y_test = dealdata(data, target)
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.tree import DecisionTreeClassifier
    clf = AdaBoostClassifier(DecisionTreeClassifier(max_depth=62), algorithm="SAMME", n_estimators=120, learning_rate=1)

    clf = clf.fit(X_train, y_train)
    # importances = clf.feature_importances_
    # indices = np.argsort(importances)[::-1]
    # size = len(feature_name)
    # Print the feature ranking
    # print(str(size)+" criterion='gini', Feature ranking:")
    # for f in range(size):
    #     print("feature name: %s <==> importances rate: (%f)" % (feature_name[indices[f]], importances[indices[f]]))

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
    data, target = loadDataSet(filepath2)
    dataArr, testArr, classLabels, testLabelArr = dealdata(data, target)
    bdt = AdaBoostClassifier(DecisionTreeClassifier(max_depth=62), algorithm="SAMME", n_estimators=30)
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
    size = len(feature_name)
    # importances = clf.feature_importances_
    # indices = np.argsort(importances)[::-1]
    # size = len(feature_name)
    # Print the feature ranking
    # print(str(size)+" criterion='gini', Feature ranking:")
    # for f in range(size):
    #     print("feature name: %s <==> importances rate: (%f)" % (feature_name[indices[f]], importances[indices[f]]))

    # from sklearn.externals import joblib
    # #保存模型
    # joblib.dump(clf, "./sklearn_result01/dx_train_model.m", compress=3)
    # clf = joblib.load("./sklearn_result01/dx_train_model.m")
    evaluate_function(bdt, testArr, testLabelArr)
    # plot_fig("./sklearn_result01/dx_fig01")


def xgboost_train():
    target_names = ['label is 2', 'label is 1']
    import xgboost as xgb
    dataMat, labelMat = loadDataSet(filepath2)
    dataMat = np.array(dataMat)
    labelMat = np.array(labelMat)
    labelMat = np.where(labelMat < 2, labelMat, 0)
    X_train, X_test, y_train, y_test = dealdata(dataMat, labelMat)
    max_depth = 10
    subsample = 0.95
    num_round = 2000
    early_stopping_rounds = 50
    params = {'max_depth': max_depth, 'eta': 0.1, 'silent': 1, 'alpha': 0.5, 'lambda': 0.5,
              'eval_metric': 'auc', 'subsample': subsample, 'objective': 'binary:logistic'}
    num_round = num_round
    early_stopping_rounds = early_stopping_rounds
    clf = xgb.XGBClassifier(learning_rate=0.1,
                            n_estimators=30,
                            max_depth=40,
                            min_child_weight=1,
                            gamma=0.15,
                            subsample=0.8,
                            colsample_bytree=0.8,
                            nthread=4,
                            scale_pos_weight=1,
                            seed=27)
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
    labelMat = np.where(labelMat < 2, labelMat, 0)
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

    dx_train()
    # dx_train2()
    # sklearn_single_classficatopn_test()
    # print ("AdaBoost:")
    # AdaBoost_dx_train()
    # ensemble_train()
    # GridSearch_train()
    # voting_train()

    # xgboost_train()
    # print ("lightgbm:")
    # lightgbm_train()
    # feature_importance()
