
准确率： 83.1674%
微平均，精确率： 83.1674%
微平均，召回率： 64.4636%
微平均，调和平均数： 79.6034%
             precision    recall  f1-score   support

    class 0       0.82      0.99      0.90    207801
    class 1       0.93      0.30      0.45     62662

avg / total       0.85      0.83      0.80    270463

kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： 37.9582%
 
AUC面积：0.725499437451
---------------------------------------------------------------
召回率：0.993176163733572
精度：0.993176163733572
调和平均数：0.9931761637335719

三、随机深林：正负样本1:1，训练集与测试集比例7:3
训练结果：
```
Feature ranking:
1. judgedoc_is_no: 12 (0.535764)
2. judgedoc_cnt: 0 (0.277112)
3. litigant_defendant_cnt: 18 (0.053607)
4. near_3_year_judgedoc_cnt: 21 (0.018144)
5. near_2_year_judgedoc_cnt: 6 (0.015649)
6. near_1_year_judgedoc_cnt: 13 (0.015415)
7. litigant_defendant_contract_dispute_cnt: 1 (0.012496)
8. litigant_defendant_bust_cnt: 3 (0.012410)
9. litigant_defendant_infringe_cnt: 11 (0.010188)
10. litigant_defendant_Intellectual_property_owner_cnt: 4 (0.009667)
11. litigant_defendant_unjust_enrich_cnt: 5 (0.007899)
12. litigant_result_sum_money: 15 (0.004442)
13. net_judgedoc_defendant_cnt: 19 (0.003896)
14. shixin_is_no: 16 (0.003261)
15. shixin_cnt: 8 (0.003250)
16. near_3_year_shixin_cnt: 23 (0.003127)
17. near_2_year_shixin_cnt: 17 (0.002818)
18. near_1_year_shixin_cnt: 22 (0.002755)
19. court_announce_is_no: 14 (0.002751)
20. court_announce_cnt: 20 (0.002668)
21. court_announce_litigant_cnt: 10 (0.001130)
22. court_notice_is_no: 9 (0.000972)
23. court_notice_cnt: 7 (0.000581)
24. court_notice_litigant_cnt: 2 (0.000000)
准确率： 64.7331%
微平均，精确率： 64.7331%
微平均，召回率： 64.7786%
微平均，调和平均数： 62.1267%
             precision    recall  f1-score   support

 label is 0       0.60      0.91      0.72     62814
 label is 1       0.81      0.39      0.52     63032

avg / total       0.70      0.65      0.62    125846

kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： 29.5302%
auc_area:0.729079139276

Process finished with exit code 0
```