#!---* coding: utf-8 --*--
#!/usr/bin/python
'''
上述模型在测试的时候，为每个股票打了一个分数，可以认为是将输入的70个因子转换成了一个集成的“因子”，现在让我们来检测这个非线性输出的因子回测效果如何。
本文选取了中证500作为基准，并分为5组查看每类效果。回测框架参考优矿API文档 中quick_backtest参数优化，画图参考之前社区贴凤鸣朝阳 - 股价日内模式分析
'''
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt

def back_factor():
    signal_df = pd.read_csv(u'./raw_data/factor.csv', dtype={"ticker": np.str, "tradeDate": np.str}, index_col=0,
                            encoding='GBK')
    signal_df['ticker'] = signal_df['ticker'].apply(lambda x: x + '.XSHG' if x[:2] in ['60'] else x + '.XSHE')
    signal_df = signal_df[[u'ticker', u'tradeDate', u'factor']]

    # 申万行业
    sw_frame = signal_df(industryVersionCD=u"010303", industry=u"", secID=u"", ticker=u"", intoDate=u"",
                                      field=u"", pandas="1")
    sw_frame = sw_frame[sw_frame.isNew == 1][['secID', 'ticker', 'industryName1', 'industryName2', 'industryName3']]
    sw_frame = sw_frame[['secID', 'industryName1']]
    sw_frame.columns = ['ticker', 'industryName1']
    signal_df = signal_df.merge(sw_frame, on=['ticker'], how='left')
    signal_df.head()

if __name__ == '__main__':
    back_factor()