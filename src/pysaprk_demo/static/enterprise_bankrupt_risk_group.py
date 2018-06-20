#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 
@site: 
@software: PyCharm
@file: enterprise_bankrupt_risk_group.py
@time: 18-6-12 下午4:42
"""
import traceback

import pandas as pd


def get_company_names01(path):
    """
    读取txt文本
    :param path:
    :return:
    """
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
    "/home/sinly/ljtstudy/code/ML_work/src/pysaprk_demo/data/bankrupt_company_ok.txt")

file_path = "/home/sinly/ljtstudy/back/new_version_all_features.csv"
feature_name = ["regcap", "established_years", "industry_dx_rate", "industry_all_cnt", "industry_dx_cnt",
                "net_judgedoc_defendant_cnt", "fr_change_cnt", "share_change_cnt", "judgedoc_cnt", "zhixing_cnt",
                "trade_mark_cnt", "address_change_cnt", "network_share_zhixing_cnt", "shixin_cnt", "_c1",
                "litigant_defendant_contract_dispute_cnt", "court_notice_is_no", "network_share_judge_doc_cnt",
                "litigant_defendant_bust_cnt"]

save_bankrupt_csv_path = "/home/sinly/ljtstudy/back/enterprise_bankrupt_predict_result.csv"
def string_list_to_float(list01):
    res = []
    for item in list01:
        try:
            res.append(float(item))
        except:
            # print(item)
            res.append(0.0)
    return res


def validate_model(clf, data):
    """

    :param clf:
    :param data:
    :return:
    """
    try:
        bankrupt_company_list = []
        is_bankrupt_list = []
        bankrupt_predictt_proba_list = []
        bankrupt_predictt_list = []
        features_list = []
        company_list = data["_c0"].tolist()
        df = data
        df1 = df[feature_name].apply(lambda x: string_list_to_float(x))
        df[feature_name] = df1
        df = df.fillna(0)
        for company in company_list:
            feature = df[df["_c0"] == company][feature_name]
            feature = feature[feature_name].as_matrix()
            is_bankrupt = df[df["_c0"] == company]['is_bankrupt'].values[0]
            # clf.predict(feature)
            bankrupt_predict_proba = clf.predict_proba(feature)[0][0]
            bankrupt_predict = clf.predict(feature)[0]
            bankrupt_company_list.append(company)
            is_bankrupt_list.append(is_bankrupt)
            bankrupt_predictt_proba_list.append(bankrupt_predict_proba)
            bankrupt_predictt_list.append(bankrupt_predict)
            features_list.append(str(feature[0]))
        c = {"company": company_list,
             "predict": bankrupt_predictt_list,
             "predict_proba": bankrupt_predictt_proba_list,
             "is_bankrupt": is_bankrupt_list,
             "features": features_list
             }
        df_csv = pd.DataFrame(c)
        df_csv.to_csv(save_bankrupt_csv_path)
    except Exception as e:
        traceback.print_exc()


def load_model(model_name):
    from sklearn.externals import joblib
    return joblib.load(model_name)


def get_data():
    df = pd.read_csv(file_path)
    # 正常
    is_bankrupt_df = df['_c0'].isin([bankrupt_company_list01])
    sampling = df[(True ^ is_bankrupt_df)]
    df_bankrupt = df[(False ^ is_bankrupt_df)]
    del df
    df_normal = sampling[sampling['_c1'] == 1].sample(n=7829)
    df_normal['is_bankrupt'] = 1
    df_bankrupt['is_bankrupt'] = 0
    # df_n.insert(0, 'is_bankrupt')
    frames = [df_normal, df_bankrupt]
    df = pd.concat(frames)
    del df_normal
    del df_bankrupt
    df = df.fillna(0)
    # df = df[feature_name].apply(lambda x: string_list_to_float(x))
    clf = load_model("/home/sinly/ljtstudy/code/ML_work/src/decision_tree/bankrupt_company_predict_model.m")
    validate_model(clf, df)


def fig_pro_distribution():
    """
    企业破产预测分布
    """
    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    # Load data
    df = pd.read_csv(save_bankrupt_csv_path)
    X = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    Y = []
    df['predict_proba'] = df['predict_proba'].apply(lambda x: round(x,1))
    for x in X:
        y = df[df['predict_proba'] == x]['predict_proba'].count()
        Y.append(y)
    print(X)
    print(Y)
     # the histogram of the data
    n, bins, patches = ax.hist(X, 10)
    ax.plot(bins, Y, '--')
    plt.plot(X, Y, 'o-')
    ax.set_xlabel('Probably')
    ax.set_ylabel('number')
    plt.suptitle("enterprise bankrupt probably distribution")
    fig.tight_layout()
    plt.legend()
    plt.show()


def fig_demo():
    import matplotlib
    import numpy as np
    import matplotlib.pyplot as plt

    np.random.seed(19680801)

    # example data
    mu = 100  # mean of distribution
    sigma = 15  # standard deviation of distribution
    x = mu + sigma * np.random.randn(437)

    num_bins = 50

    fig, ax = plt.subplots()

    # the histogram of the data
    n, bins, patches = ax.hist(x, num_bins)

    # add a 'best fit' line
    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
         np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2))
    ax.plot(bins, y, '--')

    ax.set_xlabel('Smarts')
    ax.set_ylabel('Probability density')
    ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

    # Tweak spacing to prevent clipping of ylabel
    fig.tight_layout()
    plt.show()
    
    
def bankrupt_prob_distribution_by_division_split():
    """
    按[0.01, 0.05, 0.2, 0.4, 0.5, 0.6]
    比例划分区间
    :return:
    """
    df = pd.read_csv(save_bankrupt_csv_path)
    # c = [1, 0.85, 0.75, 0.65, 0.55, 0.45, 0.35, 0.25, 0.15, 0]
    # c = [1, 0.85, 0.75, 0.55,0.35,0.15, 0]
    C = [1.0,  0.97,    0.55, 0.35, 0.1, 0.04,0]
    # a = [0, 0.01, 0.05, 0.2, 0.4, 0.5,1.0]
    # b = ['极高风险', '高风险', '次高风险', '一般风险', '低风险', '极低风险']
    df['predict_proba'] = df['predict_proba'].astype('float64')
    all_proba_avg = df['predict_proba'].mean()
    print("总体破产预测平均值为%f" % (all_proba_avg))
    for i in range(6):
        df01 = df[(df['predict_proba']< C[i]) & (df['predict_proba']> C[i+1])]
        count1 = df01['predict_proba'].count()
        predict_proba_avg = df01['predict_proba'].mean()
        count2 = df01[df01['is_bankrupt'] == 0]['predict_proba'].count()

        print("破产概率区间为(%f,%f]" % (C[i+1], C[i]))
        print("破产公司的数量为%d" % (count2))
        print("区间公司的数量为%d" % (count1))
        print("区间内实际破产占的比重为%f" % (count2 / float(count1)))
        print("区间预测平均值为%f" % (predict_proba_avg))
        print("区间内破产的比重是平均破产概率的%f倍"%((round(predict_proba_avg / all_proba_avg, 2))))
        print('\n')

if __name__ == '__main__':
    get_data()
    # fig_demo()
    # fig_pro_distribution()
    # bankrupt_prob_distribution_by_division_split()
