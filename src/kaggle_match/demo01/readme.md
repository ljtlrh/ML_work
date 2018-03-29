给用户推荐商品
地址：
http://blog.csdn.net/qq_34264472/article/details/53808876
https://www.kaggle.com/c/santander-product-recommendation/data
描述：
根据用户15个月商品购买记录（2015年1月28日到2016年5月用户购买商品记录），预测下个月（2016年6月）哪些用户最可能购买的7个商品。

思路
https://www.kaggle.com/c/santander-product-recommendation/discussion/25579

融合模型。

模型融合算法效果不好。商品分布跟月份相关，只使用2015年6月的测试数据来预测2016年6月份的用户购买行为。数据量大大缩小。
有的用户2015年6月之后才有信息记录，还是用2016年5月预测
模型融合。
2015年6月和2016年5月都出现，融合
2015年6月和2016年5月只出现一次，当作结果
2015年6月和2016年5月都不出现，预测不购买
不预测你购买商品，而是假定用户购买商品，预测用户会购买哪些商品。multi:softprob。

xgb_params = {
    'seed': 0,
    'silent': 1,
    'objective': 'multi:softprob', #reg:linear, binary:logistic,multi:softmax,multi:softprob
    'eval_metric': 'mlogloss', #rmse, mae,logloss,error,merror,mlogloss,auc
    'num_class': 4,# multi:softmax需要此参数
    'max_depth': 4,
    'min_child_weight': 1,
    'subsample': 0.7,
    'colsample_bytree': 0.7,
    'learning_rate': 0.075, # eta
    'gamma': 0.01,
    'alpha': 0.01,
    'lambda': 0.01,
    'nthread': 4,
    'nrounds': 500
}
每条记录用户购买了多个商品，将该记录拆分多条，每条记录一个商品

train取出labelY，按asix=0轴拼接train、test集，一起预处理。

seaborn使用scatter图。

方差越来越大。log。证明
几个偏差特别大的噪声点。如果在train，直接去除，如果在test，赋值na，后边会单独处理na值
seaborn使用heatmap图，

查看特征相关Pearson系数，相关较大的，去除一列，先效果。
降维效果不好。去除几列与结果关系不大的列
非数值类型转数值类型。

有的样本在train全，test有缺失值。

heatmap图，相关性较大的列的值处理后填充
rf预测
好多列的数据都缺失，直接删除该样本。
去除缺失值特别多的列。

特征组合。比如工资和退休金组合。房屋信息、几个车库。

参数调整。GridSearchCV。

K折交叉验证。sklearn.cross_validation.KFold

