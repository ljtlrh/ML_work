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

def get_company_names01(path):
    company_names = []
    with open(path) as f:
        for data in f.readlines():
            if data.startswith('#'):
                continue
            name = data.decode('utf-8')
            # print name
            company_names.append(name.strip("\n"))
    return company_names

bankrupt_company_list01 = get_company_names01(
    "/home/sinly/ljtstudy/code/ML_work/src/pysaprk_demo/data/bankrupt_company.txt")
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
file_path = "/home/sinly/ljtstudy/back/new_version_all_features.csv"
filepath2 = "data_dx2_zc03.txt"
feature_name = ["_c1", "network_share_shixin_cnt", "network_share_zhixing_cnt", "network_share_sszc_cnt",
                "network_share_punish_cnt",
                "network_share_judge_doc_cnt", "network_share_cancel_cnt", "judgedoc_is_no", "judgedoc_cnt",
                "litigant_defendant_cnt",
                "near_3_year_judgedoc_cnt", "near_2_year_judgedoc_cnt", "near_1_year_judgedoc_cnt",
                "litigant_defendant_contract_dispute_cnt", "litigant_defendant_bust_cnt",
                "litigant_defendant_infringe_cnt", "litigant_defendant_Intellectual_property_owner_cnt",
                "litigant_defendant_unjust_enrich_cnt", "litigant_result_sum_money",
                "net_judgedoc_defendant_cnt", "shixin_is_no", "shixin_cnt", "near_3_year_shixin_cnt",
                "near_2_year_shixin_cnt", "near_1_year_shixin_cnt", "court_announce_is_no",
                "court_announce_cnt", "court_announce_litigant_cnt", "court_notice_is_no", "court_notice_cnt",
                "court_notice_litigant_cnt", "regcap",
                "zczjbz", "established_years", "fr_change_cnt", "address_change_cnt", "regcap_change_cnt",
                "share_change_cnt", "network_fr_share_change_cnt", "hy_shixin_cnt", "zhixing_cnt",
                "sszc_cnt", "punish_cnt", "judge_doc_cnt", "cancel_cnt", "bidding_cnt", "bidding_three_year_rate",
                "is_black_list", "is_escape", "is_diff_raise_money", "is_stop_busi", "is_lost_with_money",
                "is_just_lost", "invent_publish_cnt", "invent_patent_cnt", "utility_publish_cnt",
                "invent_publish_three_year_rate", "invent_patent_three_year_rate", "utility_publish_three_year_rate",
                "warn_cnt", "fine_cnt", "revoking_cnt", "warn_cnt_three_year_rate", "fine_cnt_three_year_rate",
                "revoking_cnt_three_year_rate", "estate_auction_cnt", "real_estate_auction_cnt", "trade_mark_cnt",
                "trademark_three_year_rate", "industry_13", "industry_26", "industry_519", "industry_18",
                "industry_1810", "industry_62", "industry_dx_rate", "industry_dx_cnt", "industry_all_cnt"]

feature_name = ["regcap",  "established_years",  "industry_dx_rate",  "industry_all_cnt",  "industry_dx_cnt",  "net_judgedoc_defendant_cnt",  "fr_change_cnt",  "share_change_cnt",  "network_share_judge_doc_cnt",  "regcap_change_cnt", "court_notice_is_no", "judgedoc_cnt", "address_change_cnt", "network_share_zhixing_cnt", "trade_mark_cnt", "cancel_cnt", "network_share_cancel_cnt", "litigant_result_sum_money", "litigant_defendant_bust_cnt", "zhixing_cnt", "judge_doc_cnt", "zczjbz", "near_3_year_judgedoc_cnt", "court_announce_litigant_cnt", "bidding_cnt", "litigant_defendant_contract_dispute_cnt", "network_share_shixin_cnt", "near_2_year_judgedoc_cnt",  "litigant_defendant_unjust_enrich_cnt",  "near_3_year_shixin_cnt",  "hy_shixin_cnt",  "network_share_sszc_cnt",  "estate_auction_cnt",  "shixin_is_no",  "invent_patent_cnt",  "litigant_defendant_infringe_cnt",  "utility_publish_cnt",  "shixin_cnt",  "near_1_year_judgedoc_cnt",  "near_1_year_shixin_cnt",  "court_notice_cnt",  "court_notice_litigant_cnt",    "court_announce_is_no",  "fine_cnt",  "court_announce_cnt",  "sszc_cnt",  "near_2_year_shixin_cnt",  "invent_publish_cnt",  "real_estate_auction_cnt"]

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
    f = open(path, 'a')
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
    """

    :param y:
    :param pred:
    :return:
    """
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


def feature_importance(clf, feature_name01, X_test, y_test):
    save_model(clf)
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    size = len(feature_name01)
    # Print the feature ranking
    print(str(size) + " Feature ranking:")

    for f in range(size):
        print("%d feature name: %s <==> importances rate: (%f)" % (
        f, feature_name01[indices[f]], importances[indices[f]]))

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
    target_names = ['label is 0', 'label is 1']
    print(classification_report(y_test, ytestPre, target_names=target_names))
    from sklearn.metrics import cohen_kappa_score
    kappa_score = cohen_kappa_score(y_test, ytestPre)
    print(u'kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： %.4f%%' % (100 * kappa_score))
    pre_result = clf.predict_proba(X_test)
    ROC_AUC(y_test, pre_result)
    # dtp = DecisionTreeClassifierParser(clf, feature_name01)
    # res = dtp.get_parsed_tree()
    # write_json("/home/sinly/ljtstudy/code/risk_rules/sklearn_result01/bankrupt_risk_rule.json", res)
    # print (json.dumps(res, ensure_ascii=False, indent=4))


def string_to_float(data):
    try:
        return float(data)
    except:
        print(data)
        return 0


def string_list_to_float(list01):
    res = []
    for item in list01:
        try:
            res.append(float(item))
        except:
            # print(item)
            res.append(0.0)
    return res


def is_rmb(x):
    if x == 156 or x == 0:
        return 1
    else:
        return 0


def write_txt(path, data):
    '''
     保存清洗数据
    '''
    f = open(path, 'w')
    f.write(data.decode('unicode_escape'))
    f.write('\n')  # write不会在自动行末加换行符，需要手动加上
    f.flush()
    f.close()


def write_json(path, data):
    '''
     保存清洗数据
    '''
    import traceback
    try:
        with open(path, "w") as outfile:
            json.dump(data, outfile, indent=4)
    except Exception as e:
        traceback.print_exc()


def save_model(dx_tree):
    from sklearn.externals import joblib
    joblib.dump(dx_tree, 'bankrupt_tree.model')


def bankrupt_train():
    """

    :return:
    """
    df = pd.read_csv(file_path)
    # 正常
    df_normal = df[df['_c1'] == 1].sample(n=4871)
    df_normal['is_bankrupt'] = 1
    # 吊销
    # df_n = df[df['_c1'] == 2].head(389081)
    # 破产
    df_n = df[df['_c0'].map(lambda x: x in bankrupt_company_list01)]
    df_n['is_bankrupt'] = 0
    frames = [df_normal, df_n]
    df = pd.concat(frames)
    del df_normal
    del df_n
    df = df.fillna(0)
    target = df['is_bankrupt'].as_matrix()
    target = pd.to_numeric(target, errors='coerce')
    # data = pd.DataFrame()
    feature_name01 = feature_name[1:]
    df = df[feature_name01].apply(lambda x: string_list_to_float(x))
    df['zczjbz'] = df.zczjbz.apply(lambda x: is_rmb(x))
    # zczjbz = set(df['zczjbz'].tolist())
    # print("zczjbz"+str(zczjbz))
    data = df.as_matrix()
    del df
    # for item in feature_name01:
    #     data[item] = df[item].apply(lambda x: string_to_float(x))
    # data = data.as_matrix()
    # [rows, cols] = data.shape
    # data = [[string_to_float(row[col]) for row in data] for col in range(rows - 1)]
    # data = np.array(data)
    # data = df[feature_name[1:]].astype(float, errors='ignore').as_matrix()
    X_train, X_test, y_train, y_test = dealdata(data, target)
    # from sklearn.ensemble import ExtraTreesClassifier
    # 决策树
    # clf = tree.DecisionTreeClassifier(max_depth=77, splitter="best",
    #                                   max_features=77, min_samples_split=77,
    #                                   max_leaf_nodes=1000)
    # clf = clf.fit(X_train, y_train)
    # xgboost
    import xgboost as xgb
    clf = xgb.XGBClassifier(learning_rate=0.1,
                            n_estimators=30,
                            max_depth=43,
                            min_child_weight=1,
                            gamma=0.15,
                            subsample=0.8,
                            colsample_bytree=0.8,
                            nthread=4,
                            scale_pos_weight=1,
                            seed=27)
    clf.fit(X_train, y_train, early_stopping_rounds=100, eval_metric="auc",
            eval_set=[(X_test, y_test)])
    save_model(clf)
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]
    size = len(feature_name01)
    # Print the feature ranking
    print(str(size) + " Feature ranking:")

    for f in range(size):
        print("%d feature name: %s <==> importances rate: (%f)" % (
        f, feature_name01[indices[f]], importances[indices[f]]))

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
    target_names = ['label is 0', 'label is 1']
    print(classification_report(y_test, ytestPre, target_names=target_names))
    from sklearn.metrics import cohen_kappa_score
    kappa_score = cohen_kappa_score(y_test, ytestPre)
    print(u'kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： %.4f%%' % (100 * kappa_score))
    pre_result = clf.predict_proba(X_test)
    ROC_AUC(y_test, pre_result)
    # dtp = DecisionTreeClassifierParser(clf, feature_name01)
    # res = dtp.get_parsed_tree()
    # write_json("/home/sinly/ljtstudy/code/risk_rules/sklearn_result01/bankrupt_risk_rule.json", res)
    # print (json.dumps(res, ensure_ascii=False, indent=4))


def validate_model(clf, data):
    """

    :param clf:
    :param data:
    :return:
    """
    global bankrupt_company_list01
    bankrupt_company_list01_list = []
    company_list = data["_c0"].tolist()
    df = data
    df1 = df[feature_name].apply(lambda x: string_list_to_float(x))
    df[feature_name] = df1
    df['zczjbz'] = df.zczjbz.apply(lambda x: is_rmb(x))
    df = df.fillna(0)
    for company in company_list:
        feature = df[df["_c0"] == company][feature_name]
        clf.predict(feature)
        mode_predict_proba = clf.predict_proba(feature[feature_name].as_matrix())[0]
        # mode_predict = clf.predict(feature[feature_name].as_matrix())[0]
        if mode_predict_proba[0] > 0.6:
            # companys = get_bankrupt_company_list01_name(company)
            bankrupt_company_list01_list.append(company)
            # time.sleep(200)
        else:
            continue
    bankrupt_company_list01_list = list(set(bankrupt_company_list01_list))
    bankrupt_company_list01.extend(bankrupt_company_list01_list)
    bankrupt_company_list01 = list(set(bankrupt_company_list01))
    print(bankrupt_company_list01.__len__())
    print (json.dumps(bankrupt_company_list01, ensure_ascii=False, indent=4))
    f1 = open('/home/sinly/ljtstudy/code/ML_work/src/pysaprk_demo/data/bankrupt_company.txt', 'w')

    for company in bankrupt_company_list01:
        company = company+"\n"
        f1.write(company)

    f1.flush()
    f1.close()
    # bankrupt_train_lightgbm()



def bankrupt_train_lightgbm():
    """

    :return:
    """
    df = pd.read_csv(file_path)
    # 正常
    df_normal = df[df['_c0'].map(lambda x: x not in bankrupt_company_list01)]
    df_normal =df_normal.sample(n=int(6700))
    df_vail =df_normal.sample(n=int(6700))
    df_normal['is_bankrupt'] = 1
    # 吊销
    # df_n = df[df['_c1'] == 2].head(389081)
    # 破产
    df_n = df[df['_c0'].map(lambda x: x in bankrupt_company_list01)]
    df_n['is_bankrupt'] = 0
    frames = [df_normal, df_n]
    df = pd.concat(frames)
    del df_normal
    del df_n
    df = df.fillna(0)
    target = df['is_bankrupt'].as_matrix()
    target = pd.to_numeric(target, errors='coerce')
    # data = pd.DataFrame()
    feature_name01 = feature_name
    df = df[feature_name01].apply(lambda x: string_list_to_float(x))
    df['zczjbz'] = df.zczjbz.apply(lambda x: is_rmb(x))
    # zczjbz = set(df['zczjbz'].tolist())
    # print("zczjbz"+str(zczjbz))
    data = df.as_matrix()
    del df
    # for item in feature_name01:
    #     data[item] = df[item].apply(lambda x: string_to_float(x))
    # data = data.as_matrix()
    # [rows, cols] = data.shape
    # data = [[string_to_float(row[col]) for row in data] for col in range(rows - 1)]
    # data = np.array(data)
    # data = df[feature_name[1:]].astype(float, errors='ignore').as_matrix()
    X_train, X_test, y_train, y_test = dealdata(data, target)
    # from sklearn.ensemble import ExtraTreesClassifier
    # 决策树
    # clf = tree.DecisionTreeClassifier(max_depth=77, splitter="best",
    #                                   max_features=77, min_samples_split=77,
    #                                   max_leaf_nodes=1000)
    # clf = clf.fit(X_train, y_train)
    # lightgbm
    import lightgbm
    # clf = lightgbm.LGBMClassifier(boosting_type='gbdt', #
    #                               num_leaves=20,#决策树的叶子节点
    #                               objective='binary',#目标为二分类
    #                               max_depth=6,
    #                               learning_rate=0.2,
    #                               n_estimators=1000,
    #                               metric="auc",
    #                               reg_alpha=0.1,#
    #                               subsample=0.9 #样本子集比例
    #                               )
    clf = lightgbm.LGBMClassifier(boosting_type='gbdt',
                                  colsample_bytree=1.0,
                                  learning_rate=0.2,
                                  num_leaves=10,  # 决策树的叶子节点
                                  max_depth=48,
                                  min_child_samples=8,
                                  min_child_weight=0.001,
                                  min_split_gain=0.0,
                                  n_estimators=80,
                                  n_jobs=-1,
                                  objective='binary',  #目标为二分类,
                                  reg_alpha=0.1,
                                  reg_lambda=0.0,
                                  silent=True,
                                  subsample=1.0,
                                  subsample_for_bin=200000,
                                  subsample_freq=1)

    clf.fit(X_train, y_train, early_stopping_rounds=10000, eval_metric="auc",
            eval_set=[(X_test, y_test)])
    save_model(clf)
    feature_importance(clf, feature_name01, X_test, y_test)
    validate_model(clf, df_vail)
    # print('###############################参数网格优选###################################')
    # model_gbr_GridSearch = lightgbm.LGBMClassifier()
    # # 设置参数池  参考 http://www.cnblogs.com/DjangoBlog/p/6201663.html
    # param_grid = {'n_estimators': range(30, 81, 10),
    #               'learning_rate': [0.2, 0.1, 0.05, 0.02, 0.01],
    #               'max_depth': [20, 50, 70],
    #               'num_leaves': [6, 8, 10],
    #               'reg_alpha': [0.1, 0.001, 0.005, 0.01, 0.05]
    #               }
    # # 网格调参
    # from sklearn.model_selection import GridSearchCV
    # estimator = GridSearchCV(model_gbr_GridSearch, param_grid)
    # estimator.fit(X_train, y_train.ravel())
    # print("best_estimator_:=>"+str(estimator.best_estimator_))
    # print("best param:=>"+str(estimator.best_params_))
    # print("best_index_:=>"+str(estimator.best_index_))
    # print("best_score_:=>"+str(estimator.best_score_))

    # dtp = DecisionTreeClassifierParser(clf, feature_name01)
    # res = dtp.get_parsed_tree()
    # write_json("/home/sinly/ljtstudy/code/risk_rules/sklearn_result01/bankrupt_risk_rule.json", res)
    # print (json.dumps(res, ensure_ascii=False, indent=4))


def feature_show(bst):
    """

    :param bst:
    :return:
    """
    import operator
    importance = bst.get_fscore()
    # importance = sorted(zip(), key=operator.itemgetter(1))
    importance = sorted(zip(feature_name[1:], importance.items()), key=lambda _: _[1][1], reverse=True)
    print (json.dumps(importance, ensure_ascii=False, indent=4))


def bankrupt_train_xgb():
    """

    :return:
    """
    df = pd.read_csv(file_path)
    # 正常
    df_normal = df[df['_c1'] == 1].sample(n=4871)
    df_normal['is_bankrupt'] = 1
    # 吊销
    # df_n = df[df['_c1'] == 2].head(389081)
    # 破产
    df_n = df[df['_c0'].map(lambda x: x in bankrupt_company_list01)]
    df_n['is_bankrupt'] = 0
    frames = [df_normal, df_n]
    df = pd.concat(frames)
    del df_normal
    del df_n
    df = df.fillna(0)
    target = df['is_bankrupt'].as_matrix()
    target = pd.to_numeric(target, errors='coerce')
    # data = pd.DataFrame()
    feature_name01 = feature_name[1:]
    df = df[feature_name01].apply(lambda x: string_list_to_float(x))
    df['zczjbz'] = df.zczjbz.apply(lambda x: is_rmb(x))
    # zczjbz = set(df['zczjbz'].tolist())
    # print("zczjbz"+str(zczjbz))
    data = df.as_matrix()
    del df
    # for item in feature_name01:
    #     data[item] = df[item].apply(lambda x: string_to_float(x))
    # data = data.as_matrix()
    # [rows, cols] = data.shape
    # data = [[string_to_float(row[col]) for row in data] for col in range(rows - 1)]
    # data = np.array(data)
    # data = df[feature_name[1:]].astype(float, errors='ignore').as_matrix()
    X_train, X_test, y_train, y_test = dealdata(data, target)
    # from sklearn.ensemble import ExtraTreesClassifier
    # 决策树
    # clf = tree.DecisionTreeClassifier(max_depth=77, splitter="best",
    #                                   max_features=77, min_samples_split=77,
    #                                   max_leaf_nodes=1000)
    # clf = clf.fit(X_train, y_train)
    # xgboost
    import xgboost as xgb
    # clf = xgb.XGBClassifier(learning_rate=0.1,
    #                         n_estimators=30,
    #                         max_depth=43,
    #                         min_child_weight=1,
    #                         gamma=0.15,
    #                         subsample=0.8,
    #                         colsample_bytree=0.8,
    #                         nthread=4,
    #                         scale_pos_weight=1,
    #                         seed=27)
    # clf.fit(X_train, y_train, early_stopping_rounds=100, eval_metric="auc",
    #         eval_set=[(X_test, y_test)])
    # xgb02

    # params = {
    #     "objective": 'reg:linear',
    #     "eval_metric": 'rmse',
    #     "seed": 27,
    #     "booster": "gbtree",
    #     "min_child_weight": 6,
    #     "gamma": 0.1,
    #     "max_depth": 5,
    #     "eta": 0.009,
    #     "silent": 1,
    #     "subsample": 0.65,
    #     "colsample_bytree": 0.35,
    #     "scale_pos_weight": 0.9
    # }
    # df_train = xgb.DMatrix(X_train, y_train)
    # clf = xgb.train(params, df_train, num_boost_round=10000)

    params = {
        'booster': 'gbtree',
        'objective': 'binary:logistic',
        'eta': 0.1,
        'max_depth': 40,
        'subsample': 0.8,
        'min_child_weight': 1,
        'colsample_bytree': 0.2,
        'scale_pos_weight': 0.1,
        'eval_metric': 'auc',
        'gamma': 0.2,
        'seed': 27,
        'lambda': 300
    }

    # watchlist = [(X_train, 'train'), (y_train, 'val')]
    # clf = xgb.train(params, X_train, num_boost_round=100000, evals=watchlist)

    df_train = xgb.DMatrix(X_train, y_train)
    clf = xgb.train(params, df_train, num_boost_round=10000)

    save_model(clf)

    # importances = clf.feature_importances_
    # indices = np.argsort(importances)[::-1]
    # size = len(feature_name01)
    # # Print the feature ranking
    # print(str(size) + " Feature ranking:")
    #
    # for f in range(size):
    #     print("%d feature name: %s <==> importances rate: (%f)" % (f, feature_name01[indices[f]], importances[indices[f]]))

    feature_show(bst=clf)
    X_test = xgb.DMatrix(X_test)
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
    target_names = ['label is 0', 'label is 1']
    print(classification_report(y_test, ytestPre, target_names=target_names))
    from sklearn.metrics import cohen_kappa_score
    kappa_score = cohen_kappa_score(y_test, ytestPre)
    print(u'kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： %.4f%%' % (100 * kappa_score))
    pre_result = clf.predict_proba(X_test)
    ROC_AUC(y_test, pre_result)
    # dtp = DecisionTreeClassifierParser(clf, feature_name01)
    # res = dtp.get_parsed_tree()
    # write_json("/home/sinly/ljtstudy/code/risk_rules/sklearn_result01/bankrupt_risk_rule.json", res)
    # print (json.dumps(res, ensure_ascii=False, indent=4))


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

    # bankrupt_train()
    # bankrupt_train_xgb()
    bankrupt_train_lightgbm()

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
