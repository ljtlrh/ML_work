#!---* coding: utf-8 --*--
#!/usr/bin/python
'''
Created on 2018年1月30日
 最近，人工智能引起了大家广泛的关注，其在图像识别，自然语言处理方向都做出了一些成果。该领域比较常用的模型有线性回归、树模型、SVM， 集成学习，深度学习模型(CNN, RNN)，以往大家在量化方面主要选取线性回归模型，其在解释因子收益方面比较直观，但这种做法会丧失一些非线性的特征关系。
本文主要考察集成学习在量化选股方面的运用，同上述研报一样，主要采用集成学习中的boosting方法， 选取了xgboost作为训练框架，对选取的因子进行合成，最终考察该合成因子的选股效果。
# **数据准备**
--------
本文选取了优矿的70个因子，提取股票每个月末的因子暴露作为训练输入特征。读者也可以选取自己感兴趣的因子作为基础因子。
特征按照研报中所描述做中位数去极值，缺失值处理，标准化等，该处理后的数据作为模型输入特征。同时在每个月末截面期，选取下月收益排名前30%的股票作为正例（𝑦=1），后30%的股票作为负例（𝑦=−1）。利用xgboost进行分类预测。由于处理数据源代码过长，这里不做展示，且该部分也不具备参考价值，读者可根据自己常用特征处理习惯进行处理。
@author: ljt
'''

import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt

filepath = u'../data/all_features.csv'
dxFeature = ["company_name", "judgedoc_is_no", "judgedoc_cnt", "litigant_defendant_cnt",
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

def dataread():
    # df = pd.read_csv(filepath, names=dxFeature, encoding='utf-8', header=None)
    df = pd.read_csv(filepath, header=None, names=dxFeature)
    print (df.head())
    return df


class BoostModel:
    def __init__(self, max_depth=3, subsample=0.95, num_round=2000, early_stopping_rounds=50):
        self.params = {'max_depth': max_depth, 'eta': 0.1, 'silent': 1, 'alpha': 0.5, 'lambda': 0.5,
                       'eval_metric': 'auc', 'subsample': subsample, 'objective': 'binary:logistic'}
        self.num_round = num_round
        self.early_stopping_rounds = early_stopping_rounds

    def fit(self, train_data, train_label, val_data, val_label):
        dtrain = xgb.DMatrix(train_data, label=train_label)
        deval = xgb.DMatrix(val_data, label=val_label)

        boost_model = xgb.train(self.params, dtrain, num_boost_round=self.num_round,
                                evals=[(dtrain, 'train'), (deval, 'eval')],
                                early_stopping_rounds=self.early_stopping_rounds, verbose_eval=False)
        print('get best eval auc : %s, in step %s' % (boost_model.best_score, boost_model.best_iteration))
        self.boost_model = boost_model

        return boost_model

    def predict(self, test_data):
        dtest = xgb.DMatrix(test_data)
        predict_score = self.boost_model.predict(dtest, ntree_limit=self.boost_model.best_ntree_limit)

        return predict_score


def get_train_val_test_data(year, split_pct=0.9):
    df = dataread()
    back_year = max(2007, year - 6)
    train_val_df = df[(df['year'] >= back_year) & (df['year'] < year)]
    train_val_df = train_val_df.sample(frac=1).reset_index(drop=True)

    # 拆分训练集、验证集
    train_df = train_val_df.iloc[0:int(len(train_val_df) * split_pct)]
    val_df = train_val_df.iloc[int(len(train_val_df) * split_pct):]

    test_df = df[df['year'] == year]

    return train_df, val_df, test_df


def format_feature_label(origin_df, is_filter=True):
    if is_filter:
        origin_df = origin_df[origin_df['label'] != 0]
        # 因子xgboost的label输入范围只能是[0, 1]，需要对原始label进行替换
        origin_df['label'] = origin_df['label'].replace(-1, 0)

    feature = np.array(origin_df[factors])
    label = np.array(origin_df['label'])

    return feature, label


def write_factor_to_csv(df, predict_score, year):
    # 记录模型预测分数为因子值，输出
    df['factor'] = predict_score
    df = df.loc[:, ['ticker', 'tradeDate', 'label', 'factor']]
    is_header = True
    if year != 2011:
        is_header = False

    df.to_csv('./raw_data/factor.csv', mode='a+', encoding='utf-8', header=is_header)


def pipeline():
    boost_model_list = []
    for year in range(2011, 2018):
        print('training model for %s' % year)
        train_df, val_df, test_df = get_train_val_test_data(year)
        boost_model = BoostModel()
        train_feature, train_label = format_feature_label(train_df)
        val_feature, val_label = format_feature_label(val_df)

        boost_model.fit(train_feature, train_label, val_feature, val_label)

        test_feature, test_label = format_feature_label(test_df, False)
        predict_score = boost_model.predict(test_feature)

        write_factor_to_csv(test_df, predict_score, year)
        boost_model_list.append(boost_model)

    return boost_model_list

from datetime import datetime
from sklearn.metrics import roc_auc_score
# 计算二分类模型样本外的ACC与AUC
def get_test_auc_acc():

    df = pd.read_csv('./raw_data/factor.csv')
    # 只查看原有label为+1, -1的数据
    df = df[df['label'] != 0]
    df.loc[:, 'predict'] = df.loc[:, 'factor'].apply(lambda x: 1 if x > 0.5 else -1)

    acc_list = []
    auc_list = []
    for date, group in df.groupby('tradeDate'):
        df_correct = group[group['predict'] == group['label']]
        correct = len(df_correct) * 1.0 / len(group)
        auc = roc_auc_score(np.array(group['label']), np.array(group['factor']))
        acc_list.append([date, correct])
        auc_list.append([date, auc])

    acc_list = sorted(acc_list, key=lambda x: x[0], reverse=False)
    mean_acc = sum([item[1] for item in acc_list]) / len(acc_list)

    auc_list = sorted(auc_list, key=lambda x: x[0], reverse=False)
    mean_auc = sum([item[1] for item in auc_list]) / len(auc_list)

    return acc_list, auc_list, round(mean_acc, 2), round(mean_auc, 2)


def plot_accuracy_curve():
    acc_list, auc_list, mean_acc, mean_auc = get_test_auc_acc()

    plt.plot([datetime.strptime(str(item[0]), '%Y%m%d') for item in acc_list], [item[1] for item in acc_list], '-bo')
    plt.plot([datetime.strptime(str(item[0]), '%Y%m%d') for item in auc_list], [item[1] for item in auc_list], '-ro')

    plt.legend([u"acc curve: mean_acc:%s" % mean_acc, u"auc curve: mean auc:%s" % mean_auc], loc='upper left',
               handlelength=2, handletextpad=0.5, borderpad=0.1)
    plt.ylim((0.3, 0.8))
    plt.show()


def get_feature_importance():
    df = pd.DataFrame(index=factors, columns=range(2011, 2018))
    for i, column in enumerate(range(2011, 2018)):
        feature_importance = boost_model_list[i].boost_model.get_score(importance_type='weight')
        df[column] = pd.Series(index=[factors[int(key.replace('f', ''))] for key, value in feature_importance.items()],
                               data=[value for key, value in feature_importance.items()])
        df[column] = df[column].fillna(0.0)
        df[column] = 1 + np.argsort(np.argsort(df[column]))

    df['all'] = df.mean(axis=1)

    return df.sort_values('all', ascending=False)




if __name__ == '__main__':
    dataread()
    boost_model_list = pipeline()
    plot_accuracy_curve()
    feature_importance_df = get_feature_importance()
    feature_importance_df.iloc[np.r_[0:10, -10:0]]