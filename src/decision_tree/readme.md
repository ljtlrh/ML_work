45 Feature ranking:
0  成立年限 : established_years <==> importances rate: (87.000000)
1  注册资本（量级万） : regcap <==> importances rate: (83.000000)
2  行业企业吊销率 : industry_dx_rate <==> importances rate: (54.000000)
3  行业企业数量 : industry_all_cnt <==> importances rate: (49.000000)
4  关联公司裁判文书被告次数 : net_judgedoc_defendant_cnt <==> importances rate: (37.000000)
5  行业企业吊销数量 : industry_dx_cnt <==> importances rate: (32.000000)
6  商标注册数量 : trade_mark_cnt <==> importances rate: (29.000000)
7  失信次数 : shixin_cnt <==> importances rate: (27.000000)
8  网络图法人对外投资或者任职的公司执行次数 : zhixing_cnt <==> importances rate: (26.000000)
9  是否吊销 : _c1 <==> importances rate: (26.000000)
10  (3年内)招投标次数 : bidding_cnt <==> importances rate: (26.000000)
11  裁判文书被告与破产有关纠纷次数 : litigant_defendant_bust_cnt <==> importances rate: (25.000000)
12  裁判文书次数 : judgedoc_cnt <==> importances rate: (24.000000)
13  注册资本变更次数 : regcap_change_cnt <==> importances rate: (24.000000)
14  法人变更次数 : fr_change_cnt <==> importances rate: (21.000000)
15  法院公告与否 : court_notice_is_no <==> importances rate: (20.000000)
16  网络图股东或者对外投资企业的执行次数 : network_share_zhixing_cnt <==> importances rate: (18.000000)
17  股东变更次数 : share_change_cnt <==> importances rate: (18.000000)
18  网络图法人对外投资或者任职的公司失信次数 : hy_shixin_cnt <==> importances rate: (17.000000)
19  注册资本币种 : zczjbz <==> importances rate: (16.000000)
20  裁判文书被告案件判决总金额 : litigant_result_sum_money <==> importances rate: (15.000000)
21  网络图股东或者对外投资企业有吊销企业的数量 : network_share_cancel_cnt <==> importances rate: (15.000000)
22  网络图股东或者对外投资企业作为被告的裁判文书次数 : network_share_judge_doc_cnt <==> importances rate: (15.000000)
23  裁判文书被告不当得利纠纷次数 : litigant_defendant_unjust_enrich_cnt <==> importances rate: (13.000000)
24  开庭公告被告次数 : court_announce_litigant_cnt <==> importances rate: (12.000000)
25  裁判文书被告合同纠纷次数 : litigant_defendant_contract_dispute_cnt <==> importances rate: (12.000000)
26  网络图法人对外投资或者任职的公司作为被告的裁判文书次数 : judge_doc_cnt <==> importances rate: (12.000000)
27  （3年内）动产拍卖次数 : estate_auction_cnt <==> importances rate: (11.000000)
28  裁判文书被告侵权责任纠纷次数 : litigant_defendant_infringe_cnt <==> importances rate: (11.000000)
29  网络图法人对外投资或者任职的公司有吊销企业的数量 : cancel_cnt <==> importances rate: (10.000000)
30  地址变更次数 : address_change_cnt <==> importances rate: (9.000000)
31  （3年内）不动产拍卖次数 : real_estate_auction_cnt <==> importances rate: (9.000000)
32  法院公告次数 : court_notice_cnt <==> importances rate: (7.000000)
33  (3年内)实用新型数量 : utility_publish_cnt <==> importances rate: (7.000000)
34  近3年裁判文书次数 : near_3_year_judgedoc_cnt <==> importances rate: (6.000000)
35  近2年裁判文书次数 : near_2_year_judgedoc_cnt <==> importances rate: (6.000000)
36  开庭公告次数 : court_announce_cnt <==> importances rate: (6.000000)
37  网络图股东或者对外投资企业的失信次数 : network_share_shixin_cnt <==> importances rate: (6.000000)
38  (3年内)发明专利数量 : invent_patent_cnt <==> importances rate: (5.000000)
39  (3年内)发明公布数量 : invent_publish_cnt <==> importances rate: (5.000000)
40  网络图法人对外投资或者任职的公司司法拍卖 : sszc_cnt <==> importances rate: (5.000000)
41  近1年裁判文书次数 : near_1_year_judgedoc_cnt <==> importances rate: (5.000000)
42  近3年内失信次数 : near_3_year_shixin_cnt <==> importances rate: (4.000000)
43  法院公告被告次数 : court_notice_litigant_cnt <==> importances rate: (3.000000)
44  网络图股东或者对外投资企业司法拍卖 : network_share_sszc_cnt <==> importances rate: (2.000000)
准确率： 84.8905%
微平均，精确率： 84.8905%
微平均，召回率： 84.6184%
微平均，调和平均数： 84.8415%
             precision    recall  f1-score   support

 label is 0       0.86      0.80      0.83      2266
 label is 1       0.84      0.89      0.86      2572

avg / total       0.85      0.85      0.85      4838

kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： 69.5307%
auc_area:0.923086340233
