决策树:
4 Feature ranking:
feature name: TUTag <==> importances rate: (0.896184)
feature name: MonthU <==> importances rate: (0.103816)
feature name: TagU <==> importances rate: (0.000000)
feature name: UTag <==> importances rate: (0.000000)
准确率： 83.4175%
微平均，精确率： 83.4175%
微平均，召回率： 24.2417%
微平均，调和平均数： 78.7215%
             precision    recall  f1-score   support

        HP0       0.00      0.00      0.00        53
     HP1225       0.00      0.00      0.00       203
       HP16       0.96      0.98      0.97      1900
     HP2000       0.00      0.00      0.00        36
     HP2010       0.00      0.00      0.00        11
     HP2074       0.00      0.00      0.00        25
       HP78       0.45      0.96      0.61       299
      HP820       0.00      0.00      0.00        48

avg / total       0.76      0.83      0.79      2575

kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： 60.2251%

随机森林:
4 Feature ranking:
feature name: TUTag <==> importances rate: (0.634589)
feature name: MonthU <==> importances rate: (0.236360)
feature name: TagU <==> importances rate: (0.070674)
feature name: UTag <==> importances rate: (0.058376)
准确率： 91.4951%
微平均，精确率： 91.4951%
微平均，召回率： 54.0289%
微平均，调和平均数： 91.0290% 

avg / total       0.91      0.91      0.91      2575 
kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： 80.3231%