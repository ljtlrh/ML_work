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


/usr/bin/python2.7 /home/sinly/ljtstudy/code/ML_work/src/decision_tree/sklearn_DT_bankrupt_79_features.py
sys:1: DtypeWarning: Columns (19) have mixed types. Specify dtype option on import or set low_memory=False.
lightgbm：
[1]	valid_0's auc: 0.893494
Training until validation scores don't improve for 10000 rounds.
[2]	valid_0's auc: 0.903088
[3]	valid_0's auc: 0.905409
[4]	valid_0's auc: 0.906543
[5]	valid_0's auc: 0.90784
[6]	valid_0's auc: 0.909528
[7]	valid_0's auc: 0.911926
[8]	valid_0's auc: 0.913636
[9]	valid_0's auc: 0.914555
[10]	valid_0's auc: 0.915793
[11]	valid_0's auc: 0.916811
[12]	valid_0's auc: 0.91696
[13]	valid_0's auc: 0.917737
[14]	valid_0's auc: 0.917705
[15]	valid_0's auc: 0.917934
[16]	valid_0's auc: 0.918028
[17]	valid_0's auc: 0.918024
[18]	valid_0's auc: 0.918228
[19]	valid_0's auc: 0.918275
[20]	valid_0's auc: 0.918486
[21]	valid_0's auc: 0.918398
[22]	valid_0's auc: 0.91844
[23]	valid_0's auc: 0.918454
[24]	valid_0's auc: 0.918791
[25]	valid_0's auc: 0.918873
[26]	valid_0's auc: 0.918807
[27]	valid_0's auc: 0.918713
[28]	valid_0's auc: 0.918533
[29]	valid_0's auc: 0.918441
[30]	valid_0's auc: 0.918394
[31]	valid_0's auc: 0.918438
[32]	valid_0's auc: 0.918527
[33]	valid_0's auc: 0.918481
[34]	valid_0's auc: 0.918508
[35]	valid_0's auc: 0.918546
[36]	valid_0's auc: 0.918415
[37]	valid_0's auc: 0.918499
[38]	valid_0's auc: 0.918363
[39]	valid_0's auc: 0.918181
[40]	valid_0's auc: 0.918052
[41]	valid_0's auc: 0.917852
[42]	valid_0's auc: 0.917806
[43]	valid_0's auc: 0.917843
[44]	valid_0's auc: 0.917963
[45]	valid_0's auc: 0.917856
[46]	valid_0's auc: 0.917764
[47]	valid_0's auc: 0.917751
[48]	valid_0's auc: 0.917835
[49]	valid_0's auc: 0.917763
[50]	valid_0's auc: 0.917682
[51]	valid_0's auc: 0.917597
[52]	valid_0's auc: 0.917501
[53]	valid_0's auc: 0.917289
[54]	valid_0's auc: 0.91728
[55]	valid_0's auc: 0.917291
[56]	valid_0's auc: 0.917304
[57]	valid_0's auc: 0.917275
[58]	valid_0's auc: 0.917204
[59]	valid_0's auc: 0.917068
[60]	valid_0's auc: 0.917003
[61]	valid_0's auc: 0.917168
[62]	valid_0's auc: 0.917111
[63]	valid_0's auc: 0.917175
[64]	valid_0's auc: 0.917254
[65]	valid_0's auc: 0.917334
[66]	valid_0's auc: 0.917275
[67]	valid_0's auc: 0.91727
[68]	valid_0's auc: 0.917144
[69]	valid_0's auc: 0.916899
[70]	valid_0's auc: 0.91686
[71]	valid_0's auc: 0.916486
[72]	valid_0's auc: 0.916511
[73]	valid_0's auc: 0.916659
[74]	valid_0's auc: 0.916652
[75]	valid_0's auc: 0.916616
[76]	valid_0's auc: 0.916661
[77]	valid_0's auc: 0.916547
[78]	valid_0's auc: 0.916498
[79]	valid_0's auc: 0.916338
[80]	valid_0's auc: 0.916299
[81]	valid_0's auc: 0.916039
[82]	valid_0's auc: 0.915897
[83]	valid_0's auc: 0.915756
[84]	valid_0's auc: 0.915764
[85]	valid_0's auc: 0.915772
[86]	valid_0's auc: 0.915755
[87]	valid_0's auc: 0.915755
[88]	valid_0's auc: 0.915638
[89]	valid_0's auc: 0.915619
[90]	valid_0's auc: 0.915554
[91]	valid_0's auc: 0.915545
[92]	valid_0's auc: 0.91566
[93]	valid_0's auc: 0.915586
[94]	valid_0's auc: 0.915341
[95]	valid_0's auc: 0.915342
[96]	valid_0's auc: 0.915235
[97]	valid_0's auc: 0.915138
[98]	valid_0's auc: 0.915137
[99]	valid_0's auc: 0.915074
[100]	valid_0's auc: 0.915107
[101]	valid_0's auc: 0.915005
[102]	valid_0's auc: 0.91499
[103]	valid_0's auc: 0.915015
[104]	valid_0's auc: 0.915128
[105]	valid_0's auc: 0.914911
[106]	valid_0's auc: 0.914881
[107]	valid_0's auc: 0.914696
[108]	valid_0's auc: 0.914667
[109]	valid_0's auc: 0.914566
[110]	valid_0's auc: 0.91471
[111]	valid_0's auc: 0.914552
[112]	valid_0's auc: 0.914442
[113]	valid_0's auc: 0.914415
[114]	valid_0's auc: 0.914244
[115]	valid_0's auc: 0.914167
[116]	valid_0's auc: 0.914119
[117]	valid_0's auc: 0.914044
[118]	valid_0's auc: 0.914035
[119]	valid_0's auc: 0.913974
[120]	valid_0's auc: 0.913922
[121]	valid_0's auc: 0.913884
[122]	valid_0's auc: 0.91374
[123]	valid_0's auc: 0.913664
[124]	valid_0's auc: 0.913701
[125]	valid_0's auc: 0.913573
[126]	valid_0's auc: 0.913468
[127]	valid_0's auc: 0.913613
[128]	valid_0's auc: 0.913668
[129]	valid_0's auc: 0.913495
[130]	valid_0's auc: 0.913417
[131]	valid_0's auc: 0.913313
[132]	valid_0's auc: 0.913272
[133]	valid_0's auc: 0.913262
[134]	valid_0's auc: 0.913156
[135]	valid_0's auc: 0.913184
[136]	valid_0's auc: 0.913117
[137]	valid_0's auc: 0.913027
[138]	valid_0's auc: 0.913173
[139]	valid_0's auc: 0.913154
[140]	valid_0's auc: 0.913067
[141]	valid_0's auc: 0.913015
[142]	valid_0's auc: 0.912914
[143]	valid_0's auc: 0.91285
[144]	valid_0's auc: 0.912801
[145]	valid_0's auc: 0.912866
[146]	valid_0's auc: 0.91294
[147]	valid_0's auc: 0.912879
[148]	valid_0's auc: 0.912772
[149]	valid_0's auc: 0.912774
[150]	valid_0's auc: 0.912664
[151]	valid_0's auc: 0.912604
[152]	valid_0's auc: 0.912637
[153]	valid_0's auc: 0.912575
[154]	valid_0's auc: 0.912526
[155]	valid_0's auc: 0.912362
[156]	valid_0's auc: 0.912423
[157]	valid_0's auc: 0.912258
[158]	valid_0's auc: 0.912114
[159]	valid_0's auc: 0.912192
[160]	valid_0's auc: 0.912011
[161]	valid_0's auc: 0.911987
[162]	valid_0's auc: 0.912034
[163]	valid_0's auc: 0.911911
[164]	valid_0's auc: 0.911999
[165]	valid_0's auc: 0.911865
[166]	valid_0's auc: 0.911723
[167]	valid_0's auc: 0.911703
[168]	valid_0's auc: 0.911725
[169]	valid_0's auc: 0.911708
[170]	valid_0's auc: 0.911753
[171]	valid_0's auc: 0.911638
[172]	valid_0's auc: 0.911593
[173]	valid_0's auc: 0.911605
[174]	valid_0's auc: 0.911577
[175]	valid_0's auc: 0.911661
[176]	valid_0's auc: 0.911698
[177]	valid_0's auc: 0.911593
[178]	valid_0's auc: 0.911554
[179]	valid_0's auc: 0.9116
[180]	valid_0's auc: 0.911651
[181]	valid_0's auc: 0.911415
[182]	valid_0's auc: 0.911452
[183]	valid_0's auc: 0.911445
[184]	valid_0's auc: 0.911435
[185]	valid_0's auc: 0.911382
[186]	valid_0's auc: 0.911307
[187]	valid_0's auc: 0.911244
[188]	valid_0's auc: 0.911129
[189]	valid_0's auc: 0.911191
[190]	valid_0's auc: 0.911136
[191]	valid_0's auc: 0.911069
[192]	valid_0's auc: 0.910871
[193]	valid_0's auc: 0.910942
[194]	valid_0's auc: 0.910754
[195]	valid_0's auc: 0.910821
[196]	valid_0's auc: 0.910785
[197]	valid_0's auc: 0.910695
[198]	valid_0's auc: 0.910528
[199]	valid_0's auc: 0.91043
[200]	valid_0's auc: 0.910469
[201]	valid_0's auc: 0.910457
[202]	valid_0's auc: 0.910347
[203]	valid_0's auc: 0.910189
[204]	valid_0's auc: 0.910183
[205]	valid_0's auc: 0.910239
[206]	valid_0's auc: 0.910142
[207]	valid_0's auc: 0.910147
[208]	valid_0's auc: 0.910068
[209]	valid_0's auc: 0.909997
[210]	valid_0's auc: 0.909973
[211]	valid_0's auc: 0.909824
[212]	valid_0's auc: 0.909845
[213]	valid_0's auc: 0.909877
[214]	valid_0's auc: 0.909876
[215]	valid_0's auc: 0.909901
[216]	valid_0's auc: 0.910002
[217]	valid_0's auc: 0.910093
[218]	valid_0's auc: 0.910181
[219]	valid_0's auc: 0.910158
[220]	valid_0's auc: 0.910236
[221]	valid_0's auc: 0.910152
[222]	valid_0's auc: 0.910133
[223]	valid_0's auc: 0.910041
[224]	valid_0's auc: 0.909948
[225]	valid_0's auc: 0.909999
[226]	valid_0's auc: 0.90999
[227]	valid_0's auc: 0.909975
[228]	valid_0's auc: 0.909946
[229]	valid_0's auc: 0.909924
[230]	valid_0's auc: 0.90987
[231]	valid_0's auc: 0.909879
[232]	valid_0's auc: 0.909815
[233]	valid_0's auc: 0.909797
[234]	valid_0's auc: 0.909755
[235]	valid_0's auc: 0.909733
[236]	valid_0's auc: 0.909635
[237]	valid_0's auc: 0.90967
[238]	valid_0's auc: 0.909618
[239]	valid_0's auc: 0.909589
[240]	valid_0's auc: 0.909583
[241]	valid_0's auc: 0.909629
[242]	valid_0's auc: 0.909592
[243]	valid_0's auc: 0.909691
[244]	valid_0's auc: 0.909699
[245]	valid_0's auc: 0.909649
[246]	valid_0's auc: 0.909611
[247]	valid_0's auc: 0.909601
[248]	valid_0's auc: 0.909685
[249]	valid_0's auc: 0.9096
[250]	valid_0's auc: 0.909543
[251]	valid_0's auc: 0.909544
[252]	valid_0's auc: 0.909502
[253]	valid_0's auc: 0.909588
[254]	valid_0's auc: 0.909567
[255]	valid_0's auc: 0.909608
[256]	valid_0's auc: 0.909566
[257]	valid_0's auc: 0.90957
[258]	valid_0's auc: 0.909612
[259]	valid_0's auc: 0.909513
[260]	valid_0's auc: 0.909442
[261]	valid_0's auc: 0.909464
[262]	valid_0's auc: 0.909512
[263]	valid_0's auc: 0.909491
[264]	valid_0's auc: 0.909443
[265]	valid_0's auc: 0.909383
[266]	valid_0's auc: 0.909297
[267]	valid_0's auc: 0.909262
[268]	valid_0's auc: 0.909225
[269]	valid_0's auc: 0.909202
[270]	valid_0's auc: 0.909149
[271]	valid_0's auc: 0.909076
[272]	valid_0's auc: 0.909103
[273]	valid_0's auc: 0.909109
[274]	valid_0's auc: 0.909093
[275]	valid_0's auc: 0.909052
[276]	valid_0's auc: 0.909019
[277]	valid_0's auc: 0.908952
[278]	valid_0's auc: 0.908826
[279]	valid_0's auc: 0.908733
[280]	valid_0's auc: 0.908679
[281]	valid_0's auc: 0.908666
[282]	valid_0's auc: 0.908652
[283]	valid_0's auc: 0.908779
[284]	valid_0's auc: 0.908632
[285]	valid_0's auc: 0.90863
[286]	valid_0's auc: 0.908667
[287]	valid_0's auc: 0.90865
[288]	valid_0's auc: 0.908689
[289]	valid_0's auc: 0.908653
[290]	valid_0's auc: 0.90871
[291]	valid_0's auc: 0.908752
[292]	valid_0's auc: 0.908736
[293]	valid_0's auc: 0.908599
[294]	valid_0's auc: 0.908687
[295]	valid_0's auc: 0.908739
[296]	valid_0's auc: 0.908739
[297]	valid_0's auc: 0.908841
[298]	valid_0's auc: 0.908899
[299]	valid_0's auc: 0.908855
[300]	valid_0's auc: 0.908752
Did not meet early stopping. Best iteration is:
[25]	valid_0's auc: 0.918873
20 Feature ranking:
0  注册资本（量级万） : regcap <==> importances rate: (99.000000)
1  成立年限 : established_years <==> importances rate: (79.000000)
2  行业企业数量 : industry_all_cnt <==> importances rate: (63.000000)
3  行业企业吊销率 : industry_dx_rate <==> importances rate: (59.000000)
4  关联公司裁判文书被告次数 : net_judgedoc_defendant_cnt <==> importances rate: (54.000000)
5  裁判文书次数 : judgedoc_cnt <==> importances rate: (46.000000)
6  法人变更次数 : fr_change_cnt <==> importances rate: (31.000000)
7  商标注册数量 : trade_mark_cnt <==> importances rate: (31.000000)
8  是否吊销 : _c1 <==> importances rate: (28.000000)
9  失信次数 : shixin_cnt <==> importances rate: (27.000000)
10  裁判文书被告案件判决总金额 : litigant_result_sum_money <==> importances rate: (27.000000)
11  网络图法人对外投资或者任职的公司执行次数 : zhixing_cnt <==> importances rate: (26.000000)
12  裁判文书被告与破产有关纠纷次数 : litigant_defendant_bust_cnt <==> importances rate: (25.000000)
13  行业企业吊销数量 : industry_dx_cnt <==> importances rate: (24.000000)
14  股东变更次数 : share_change_cnt <==> importances rate: (22.000000)
15  网络图股东或者对外投资企业的执行次数 : network_share_zhixing_cnt <==> importances rate: (22.000000)
16  裁判文书被告合同纠纷次数 : litigant_defendant_contract_dispute_cnt <==> importances rate: (18.000000)
17  法院公告与否 : court_notice_is_no <==> importances rate: (18.000000)
18  网络图股东或者对外投资企业作为被告的裁判文书次数 : network_share_judge_doc_cnt <==> importances rate: (18.000000)
19  地址变更次数 : address_change_cnt <==> importances rate: (8.000000)
准确率： 84.3425%
微平均，精确率： 84.3425%
微平均，召回率： 84.1996%
微平均，调和平均数： 84.3144%
             precision    recall  f1-score   support

 label is 0       0.86      0.81      0.83      2345
 label is 1       0.83      0.87      0.85      2560

avg / total       0.84      0.84      0.84      4905

kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： 68.5538%
auc_area:0.918872601279

Process finished with exit code 0


18 Feature ranking:
0  注册资本（量级万） : regcap <==> importances rate: (88.000000)
1  成立年限 : established_years <==> importances rate: (83.000000)
2  行业企业吊销率 : industry_dx_rate <==> importances rate: (56.000000)
3  行业企业数量 : industry_all_cnt <==> importances rate: (53.000000)
4  裁判文书次数 : judgedoc_cnt <==> importances rate: (42.000000)
5  失信次数 : shixin_cnt <==> importances rate: (42.000000)
6  关联公司裁判文书被告次数 : net_judgedoc_defendant_cnt <==> importances rate: (40.000000)
7  网络图股东或者对外投资企业的执行次数 : network_share_zhixing_cnt <==> importances rate: (31.000000)
8  是否吊销 : _c1 <==> importances rate: (29.000000)
9  法人变更次数 : fr_change_cnt <==> importances rate: (28.000000)
10  行业企业吊销数量 : industry_dx_cnt <==> importances rate: (27.000000)
11  商标注册数量 : trade_mark_cnt <==> importances rate: (25.000000)
12  网络图法人对外投资或者任职的公司执行次数 : zhixing_cnt <==> importances rate: (20.000000)
13  法院公告与否 : court_notice_is_no <==> importances rate: (17.000000)
14  地址变更次数 : address_change_cnt <==> importances rate: (15.000000)
15  网络图股东或者对外投资企业作为被告的裁判文书次数 : network_share_judge_doc_cnt <==> importances rate: (15.000000)
16  股东变更次数 : share_change_cnt <==> importances rate: (14.000000)
17  裁判文书被告合同纠纷次数 : litigant_defendant_contract_dispute_cnt <==> importances rate: (13.000000)
准确率： 84.1386%
微平均，精确率： 84.1386%
微平均，召回率： 83.9792%
微平均，调和平均数： 84.1044%
             precision    recall  f1-score   support

 label is 0       0.86      0.80      0.83      2345
 label is 1       0.83      0.88      0.85      2560

avg / total       0.84      0.84      0.84      4905

kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： 68.1340%
auc_area:0.917478344883
