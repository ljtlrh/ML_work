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
factors = [b'Beta60', b'OperatingRevenueGrowRate', b'NetProfitGrowRate', b'NetCashFlowGrowRate', b'NetProfitGrowRate5Y', b'TVSTD20',
           b'TVSTD6', b'TVMA20', b'TVMA6', b'BLEV', b'MLEV', b'CashToCurrentLiability', b'CurrentRatio', b'REC', b'DAREC', b'GREC',
           b'DASREV', b'SFY12P', b'LCAP', b'ASSI', b'LFLO', b'TA2EV', b'PEG5Y', b'PE', b'PB', b'PS', b'SalesCostRatio', b'PCF', b'CETOP',
           b'TotalProfitGrowRate', b'CTOP', b'MACD', b'DEA', b'DIFF', b'RSI', b'PSY', b'BIAS10', b'ROE', b'ROA', b'ROA5', b'ROE5',
           b'DEGM', b'GrossIncomeRatio', b'ROECut', b'NIAPCut', b'CurrentAssetsTRate', b'FixedAssetsTRate', b'FCFF', b'FCFE', b'PLRC6',
           b'REVS5', b'REVS10', b'REVS20', b'REVS60', b'HSIGMA', b'HsigmaCNE5', b'ChaikinOscillator', b'ChaikinVolatility', b'Aroon',
           b'DDI', b'MTM', b'MTMMA', b'VOL10', b'VOL20', b'VOL5', b'VOL60', b'RealizedVolatility', b'DASTD', b'DDNSR', b'Hurst']


def dataread():
    df = pd.read_csv(filepath, dtype={"ticker": np.str, "tradeDate": np.str, "next_month_end": np.str},
                     index_col=0, encoding='UTF-8')
    df.head()

if __name__ == '__main__':
    dataread()