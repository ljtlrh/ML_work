
17 Feature ranking:
feature name: established_years <==> importances rate: (0.620243)
feature name: regcap_change_cnt <==> importances rate: (0.160697)
feature name: address_change_cnt <==> importances rate: (0.063383)
feature name: judgedoc_cnt <==> importances rate: (0.042868)
feature name: cancel_cnt <==> importances rate: (0.033049)
feature name: network_share_cancel_cnt <==> importances rate: (0.029815)
feature name: bidding_cnt <==> importances rate: (0.022366)
feature name: trade_mark_cnt <==> importances rate: (0.012477)
feature name: industry_dx_rate <==> importances rate: (0.007488)
feature name: fr_change_cnt <==> importances rate: (0.004845)
feature name: share_change_cnt <==> importances rate: (0.002356)
feature name: industry_dx_cnt <==> importances rate: (0.000414)
feature name: net_judgedoc_defendant_cnt <==> importances rate: (0.000000)
feature name: network_share_zhixing_cnt <==> importances rate: (0.000000)
feature name: industry_all_cnt <==> importances rate: (0.000000)
feature name: judge_doc_cnt <==> importances rate: (0.000000)
feature name: network_share_judge_doc_cnt <==> importances rate: (0.000000)
准确率： 79.0684%
微平均，精确率： 79.0684%
微平均，召回率： 79.0671%
微平均，调和平均数： 79.0474%
             precision    recall  f1-score   support

 label is 1       0.81      0.76      0.78    128344
 label is 2       0.77      0.82      0.80    128450

avg / total       0.79      0.79      0.79    256794

kappa score是一个介于(-1, 1)之间的数. score>0.8意味着好的分类；0或更低意味着不好（实际是随机标签）： 58.1358%
auc_area:0.131654051052
[
  {
    "missclassfication_rate": 0.041724617524339362,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years > 12.5 and judgedoc_cnt <= 0.5 and bidding_cnt > 0.5",
    "sample_number": 719,
    "label": 0
  },
  {
    "missclassfication_rate": 0.013093289689034371,
    "decision_path": "regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and established_years > 16.5 and judgedoc_cnt <= 0.5 and bidding_cnt > 0.5",
    "sample_number": 611,
    "label": 0
  },
  {
    "missclassfication_rate": 0.041353383458646614,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt > 0.5 and bidding_cnt > 0.5",
    "sample_number": 532,
    "label": 0
  },
  {
    "missclassfication_rate": 0.22352410995944119,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years > 12.5 and judgedoc_cnt <= 0.5 and bidding_cnt <= 0.5 and established_years <= 17.5 and network_share_cancel_cnt <= 0.5",
    "sample_number": 37723,
    "label": 1
  },
  {
    "missclassfication_rate": 0.11109258410104632,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years > 12.5 and judgedoc_cnt <= 0.5 and bidding_cnt <= 0.5 and established_years <= 17.5 and network_share_cancel_cnt > 0.5",
    "sample_number": 23989,
    "label": 1
  },
  {
    "missclassfication_rate": 0.41536942379182157,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt <= 0.5 and trade_mark_cnt <= 2.5 and established_years <= 10.5",
    "sample_number": 17216,
    "label": 1
  },
  {
    "missclassfication_rate": 0.28750072367278412,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years <= 12.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt <= 0.5 and trade_mark_cnt <= 2.5 and established_years > 10.5",
    "sample_number": 17273,
    "label": 1
  },
  {
    "missclassfication_rate": 0.32912670368500757,
    "decision_path": "regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and established_years > 16.5 and judgedoc_cnt <= 0.5 and bidding_cnt <= 0.5 and share_change_cnt <= 2.5",
    "sample_number": 11886,
    "label": 1
  },
  {
    "missclassfication_rate": 0.42517537022603274,
    "decision_path": "regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and established_years > 16.5 and judgedoc_cnt <= 0.5 and bidding_cnt <= 0.5 and share_change_cnt > 2.5",
    "sample_number": 2566,
    "label": 0
  },
  {
    "missclassfication_rate": 0.19516945851188158,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and regcap_change_cnt <= 0.5 and network_share_cancel_cnt <= 0.5 and trade_mark_cnt > 2.5",
    "sample_number": 2567,
    "label": 0
  },
  {
    "missclassfication_rate": 0.46652067716668072,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and established_years <= 16.5 and address_change_cnt <= 0.5 and judgedoc_cnt <= 0.5 and trade_mark_cnt <= 1.5",
    "sample_number": 11873,
    "label": 0
  },
  {
    "missclassfication_rate": 0.2417096536477524,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and established_years <= 16.5 and address_change_cnt <= 0.5 and judgedoc_cnt <= 0.5 and trade_mark_cnt > 1.5",
    "sample_number": 2714,
    "label": 0
  },
  {
    "missclassfication_rate": 0.077531957481007482,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and judgedoc_cnt <= 0.5 and bidding_cnt <= 0.5 and established_years > 17.5 and fr_change_cnt <= 0.5",
    "sample_number": 65947,
    "label": 1
  },
  {
    "missclassfication_rate": 0.19248776335390508,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and judgedoc_cnt <= 0.5 and bidding_cnt <= 0.5 and established_years > 17.5 and fr_change_cnt > 0.5",
    "sample_number": 9398,
    "label": 1
  },
  {
    "missclassfication_rate": 0.01338055883510429,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 2.5 and cancel_cnt <= 1.5 and bidding_cnt > 0.5",
    "sample_number": 2541,
    "label": 0
  },
  {
    "missclassfication_rate": 0.33258232235701907,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years > 14.5 and judgedoc_cnt <= 0.5 and cancel_cnt <= 0.5 and fr_change_cnt <= 2.5 and bidding_cnt <= 0.5",
    "sample_number": 17310,
    "label": 1
  },
  {
    "missclassfication_rate": 0.018433179723502304,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years > 14.5 and judgedoc_cnt <= 0.5 and cancel_cnt <= 0.5 and fr_change_cnt <= 2.5 and bidding_cnt > 0.5",
    "sample_number": 217,
    "label": 0
  },
  {
    "missclassfication_rate": 0.43286507677229663,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt > 0.5 and bidding_cnt <= 0.5 and cancel_cnt <= 1.5 and judgedoc_cnt <= 0.5 and established_years <= 18.5",
    "sample_number": 6122,
    "label": 1
  },
  {
    "missclassfication_rate": 0.23549232497192063,
    "decision_path": "regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt > 0.5 and bidding_cnt <= 0.5 and cancel_cnt <= 1.5 and judgedoc_cnt <= 0.5 and established_years > 18.5",
    "sample_number": 2671,
    "label": 1
  },
  {
    "missclassfication_rate": 0.062128475551294346,
    "decision_path": "established_years <= 6.5 and established_years > 5.5 and address_change_cnt > 0.5",
    "sample_number": 5215,
    "label": 0
  },
  {
    "missclassfication_rate": 0.48748317631224763,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and regcap_change_cnt <= 0.5 and network_share_cancel_cnt <= 0.5 and trade_mark_cnt <= 2.5 and industry_dx_rate > 0.0528304986656 and judgedoc_cnt <= 0.5",
    "sample_number": 14860,
    "label": 0
  },
  {
    "missclassfication_rate": 0.26072607260726072,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and regcap_change_cnt <= 0.5 and network_share_cancel_cnt <= 0.5 and trade_mark_cnt <= 2.5 and industry_dx_rate > 0.0528304986656 and judgedoc_cnt > 0.5",
    "sample_number": 1515,
    "label": 0
  },
  {
    "missclassfication_rate": 0.39257028112449799,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years > 14.5 and judgedoc_cnt > 0.5 and network_share_cancel_cnt > 1.5",
    "sample_number": 996,
    "label": 1
  },
  {
    "missclassfication_rate": 0.48689516129032256,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and bidding_cnt <= 0.5 and cancel_cnt > 1.5 and judgedoc_cnt > 3.5",
    "sample_number": 992,
    "label": 1
  },
  {
    "missclassfication_rate": 0.28913443830570901,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt > 0.5 and cancel_cnt > 0.5",
    "sample_number": 2172,
    "label": 0
  },
  {
    "missclassfication_rate": 0.30442953020134228,
    "decision_path": "established_years <= 6.5 and established_years > 5.5 and address_change_cnt <= 0.5 and network_share_cancel_cnt > 0.5",
    "sample_number": 3725,
    "label": 0
  },
  {
    "missclassfication_rate": 0.29159212880143115,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and regcap_change_cnt <= 0.5 and network_share_cancel_cnt > 0.5 and trade_mark_cnt > 3.5",
    "sample_number": 559,
    "label": 0
  },
  {
    "missclassfication_rate": 0.30335365853658536,
    "decision_path": "regcap_change_cnt <= 0.5 and established_years <= 14.5 and network_share_cancel_cnt <= 0.5 and established_years > 11.5 and address_change_cnt > 1.5",
    "sample_number": 2624,
    "label": 0
  },
  {
    "missclassfication_rate": 0.3864455659697188,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years <= 12.5 and network_share_cancel_cnt > 0.5 and judgedoc_cnt <= 0.5 and trade_mark_cnt > 2.5",
    "sample_number": 1387,
    "label": 1
  },
  {
    "missclassfication_rate": 0.097593582887700536,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 2.5 and cancel_cnt <= 1.5 and bidding_cnt <= 0.5 and industry_dx_rate <= 0.0984530001879 and judgedoc_cnt > 0.5",
    "sample_number": 3740,
    "label": 0
  },
  {
    "missclassfication_rate": 0.19339622641509435,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 2.5 and cancel_cnt <= 1.5 and bidding_cnt <= 0.5 and industry_dx_rate <= 0.0984530001879 and judgedoc_cnt <= 0.5 and established_years <= 20.5",
    "sample_number": 8056,
    "label": 0
  },
  {
    "missclassfication_rate": 0.37560712358337833,
    "decision_path": "regcap_change_cnt > 2.5 and cancel_cnt <= 1.5 and bidding_cnt <= 0.5 and industry_dx_rate <= 0.0984530001879 and judgedoc_cnt <= 0.5 and established_years > 20.5",
    "sample_number": 1853,
    "label": 0
  },
  {
    "missclassfication_rate": 0.26827985270910049,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years <= 14.5 and network_share_cancel_cnt > 0.5 and cancel_cnt > 1.5",
    "sample_number": 1901,
    "label": 1
  },
  {
    "missclassfication_rate": 0.020942408376963352,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 2.5 and cancel_cnt > 1.5 and bidding_cnt > 0.5",
    "sample_number": 191,
    "label": 0
  },
  {
    "missclassfication_rate": 0.43418954827280781,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and regcap_change_cnt <= 0.5 and network_share_cancel_cnt > 0.5 and trade_mark_cnt <= 3.5 and industry_dx_rate <= 0.087636500597",
    "sample_number": 5645,
    "label": 1
  },
  {
    "missclassfication_rate": 0.28611500701262271,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and regcap_change_cnt <= 0.5 and network_share_cancel_cnt > 0.5 and trade_mark_cnt <= 3.5 and industry_dx_rate > 0.087636500597",
    "sample_number": 2852,
    "label": 1
  },
  {
    "missclassfication_rate": 0.18558006263743587,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years <= 12.5 and network_share_cancel_cnt > 0.5 and judgedoc_cnt <= 0.5 and trade_mark_cnt <= 2.5 and bidding_cnt <= 0.5",
    "sample_number": 15007,
    "label": 1
  },
  {
    "missclassfication_rate": 0.015625,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years <= 12.5 and network_share_cancel_cnt > 0.5 and judgedoc_cnt <= 0.5 and trade_mark_cnt <= 2.5 and bidding_cnt > 0.5",
    "sample_number": 64,
    "label": 0
  },
  {
    "missclassfication_rate": 0.4940231236527533,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years <= 14.5 and network_share_cancel_cnt <= 0.5 and established_years > 11.5 and address_change_cnt <= 1.5 and judgedoc_cnt <= 0.5",
    "sample_number": 5103,
    "label": 1
  },
  {
    "missclassfication_rate": 0.2244165170556553,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years <= 14.5 and network_share_cancel_cnt <= 0.5 and established_years > 11.5 and address_change_cnt <= 1.5 and judgedoc_cnt > 0.5",
    "sample_number": 557,
    "label": 0
  },
  {
    "missclassfication_rate": 0.33141210374639768,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years <= 14.5 and network_share_cancel_cnt > 0.5 and cancel_cnt <= 1.5 and trade_mark_cnt > 2.5",
    "sample_number": 694,
    "label": 0
  },
  {
    "missclassfication_rate": 0.28385228095582909,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years > 14.5 and judgedoc_cnt <= 0.5 and cancel_cnt <= 0.5 and fr_change_cnt > 2.5 and industry_dx_rate <= 0.0588655024767",
    "sample_number": 1381,
    "label": 0
  },
  {
    "missclassfication_rate": 0.46979865771812079,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years > 14.5 and judgedoc_cnt <= 0.5 and cancel_cnt <= 0.5 and fr_change_cnt > 2.5 and industry_dx_rate > 0.0588655024767",
    "sample_number": 1192,
    "label": 1
  },
  {
    "missclassfication_rate": 0.45982905982905981,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years > 12.5 and judgedoc_cnt > 0.5 and cancel_cnt <= 0.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt <= 1.5",
    "sample_number": 1170,
    "label": 0
  },
  {
    "missclassfication_rate": 0.23299492385786802,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years > 12.5 and cancel_cnt <= 0.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt > 1.5",
    "sample_number": 1970,
    "label": 0
  },
  {
    "missclassfication_rate": 0.15510697032436163,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and address_change_cnt > 0.5 and industry_dx_rate <= 0.10734000057 and established_years <= 12.5",
    "sample_number": 5796,
    "label": 0
  },
  {
    "missclassfication_rate": 0.26707159948463094,
    "decision_path": "regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and established_years <= 16.5 and address_change_cnt > 0.5 and industry_dx_rate <= 0.10734000057 and established_years > 12.5",
    "sample_number": 5433,
    "label": 0
  },
  {
    "missclassfication_rate": 0.18191841234840131,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 2.5 and cancel_cnt <= 1.5 and bidding_cnt <= 0.5 and industry_dx_rate > 0.0984530001879 and trade_mark_cnt > 1.5",
    "sample_number": 907,
    "label": 0
  },
  {
    "missclassfication_rate": 0.17445887445887445,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and network_share_cancel_cnt <= 0.5 and established_years <= 11.5 and address_change_cnt > 1.5",
    "sample_number": 2310,
    "label": 0
  },
  {
    "missclassfication_rate": 0.36290322580645162,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years > 12.5 and judgedoc_cnt > 0.5 and cancel_cnt > 0.5 and trade_mark_cnt > 2.5",
    "sample_number": 248,
    "label": 0
  },
  {
    "missclassfication_rate": 0.41093750000000001,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and regcap_change_cnt > 0.5 and network_share_cancel_cnt <= 1.5 and industry_dx_rate > 0.155301004648",
    "sample_number": 640,
    "label": 0
  },
  {
    "missclassfication_rate": 0.025763148216255978,
    "decision_path": "cancel_cnt <= 0.5 and established_years <= 4.5",
    "sample_number": 54380,
    "label": 0
  },
  {
    "missclassfication_rate": 0.071540880503144652,
    "decision_path": "established_years <= 5.5 and cancel_cnt <= 0.5 and established_years > 4.5",
    "sample_number": 21624,
    "label": 0
  },
  {
    "missclassfication_rate": 0.29290780141843969,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years > 12.5 and judgedoc_cnt > 0.5 and cancel_cnt <= 0.5 and network_share_cancel_cnt > 0.5 and judgedoc_cnt <= 5.5",
    "sample_number": 1410,
    "label": 1
  },
  {
    "missclassfication_rate": 0.36119402985074628,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years > 12.5 and cancel_cnt <= 0.5 and network_share_cancel_cnt > 0.5 and judgedoc_cnt > 5.5",
    "sample_number": 335,
    "label": 0
  },
  {
    "missclassfication_rate": 0.078090420486879544,
    "decision_path": "established_years <= 6.5 and established_years > 5.5 and address_change_cnt <= 0.5 and network_share_cancel_cnt <= 0.5 and regcap_change_cnt > 0.5",
    "sample_number": 3163,
    "label": 0
  },
  {
    "missclassfication_rate": 0.30547752808988765,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt > 0.5 and bidding_cnt <= 0.5 and cancel_cnt <= 1.5 and judgedoc_cnt > 0.5 and network_share_cancel_cnt <= 1.5",
    "sample_number": 1424,
    "label": 0
  },
  {
    "missclassfication_rate": 0.45367027677496991,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt > 0.5 and bidding_cnt <= 0.5 and cancel_cnt <= 1.5 and judgedoc_cnt > 0.5 and network_share_cancel_cnt > 1.5",
    "sample_number": 831,
    "label": 1
  },
  {
    "missclassfication_rate": 0.20569840166782488,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years > 14.5 and judgedoc_cnt > 0.5 and network_share_cancel_cnt <= 1.5 and cancel_cnt <= 0.5",
    "sample_number": 1439,
    "label": 0
  },
  {
    "missclassfication_rate": 0.47272727272727272,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years > 14.5 and judgedoc_cnt > 0.5 and network_share_cancel_cnt <= 1.5 and cancel_cnt > 0.5",
    "sample_number": 605,
    "label": 0
  },
  {
    "missclassfication_rate": 0.38346702317290554,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years <= 14.5 and network_share_cancel_cnt > 0.5 and cancel_cnt <= 1.5 and trade_mark_cnt <= 2.5 and judgedoc_cnt <= 0.5",
    "sample_number": 4488,
    "label": 1
  },
  {
    "missclassfication_rate": 0.41022592152199761,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years <= 14.5 and network_share_cancel_cnt > 0.5 and cancel_cnt <= 1.5 and trade_mark_cnt <= 2.5 and judgedoc_cnt > 0.5",
    "sample_number": 841,
    "label": 0
  },
  {
    "missclassfication_rate": 0.1488294314381271,
    "decision_path": "regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and established_years > 16.5 and judgedoc_cnt > 0.5 and network_share_cancel_cnt <= 1.5",
    "sample_number": 1794,
    "label": 0
  },
  {
    "missclassfication_rate": 0.43449781659388648,
    "decision_path": "regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and established_years > 16.5 and judgedoc_cnt > 0.5 and network_share_cancel_cnt > 1.5",
    "sample_number": 458,
    "label": 0
  },
  {
    "missclassfication_rate": 0.11592865928659286,
    "decision_path": "established_years <= 5.5 and cancel_cnt > 0.5 and network_share_cancel_cnt <= 2.5",
    "sample_number": 6504,
    "label": 0
  },
  {
    "missclassfication_rate": 0.27676620538965768,
    "decision_path": "established_years <= 5.5 and cancel_cnt > 0.5 and network_share_cancel_cnt > 2.5",
    "sample_number": 1373,
    "label": 0
  },
  {
    "missclassfication_rate": 0.39768976897689767,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and regcap_change_cnt > 0.5 and network_share_cancel_cnt > 1.5 and industry_dx_rate <= 0.105600498617",
    "sample_number": 1212,
    "label": 0
  },
  {
    "missclassfication_rate": 0.30324074074074076,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and regcap_change_cnt > 0.5 and network_share_cancel_cnt > 1.5 and industry_dx_rate > 0.105600498617",
    "sample_number": 432,
    "label": 1
  },
  {
    "missclassfication_rate": 0.059999999999999998,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years > 14.5 and judgedoc_cnt <= 0.5 and cancel_cnt > 0.5 and bidding_cnt > 0.5",
    "sample_number": 50,
    "label": 0
  },
  {
    "missclassfication_rate": 0.26685679364432674,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and bidding_cnt <= 0.5 and cancel_cnt > 1.5 and judgedoc_cnt <= 3.5 and established_years <= 18.5",
    "sample_number": 4909,
    "label": 1
  },
  {
    "missclassfication_rate": 0.14539959704499664,
    "decision_path": "regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and bidding_cnt <= 0.5 and cancel_cnt > 1.5 and judgedoc_cnt <= 3.5 and established_years > 18.5",
    "sample_number": 2978,
    "label": 1
  },
  {
    "missclassfication_rate": 0.23548991054711879,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years > 14.5 and judgedoc_cnt <= 0.5 and cancel_cnt > 0.5 and bidding_cnt <= 0.5 and cancel_cnt <= 1.5",
    "sample_number": 4807,
    "label": 1
  },
  {
    "missclassfication_rate": 0.12584327970939285,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and established_years > 14.5 and judgedoc_cnt <= 0.5 and bidding_cnt <= 0.5 and cancel_cnt > 1.5",
    "sample_number": 3854,
    "label": 1
  },
  {
    "missclassfication_rate": 0.34119960668633237,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 2.5 and cancel_cnt <= 1.5 and bidding_cnt <= 0.5 and industry_dx_rate > 0.0984530001879 and trade_mark_cnt <= 1.5 and network_share_cancel_cnt <= 0.5",
    "sample_number": 2034,
    "label": 0
  },
  {
    "missclassfication_rate": 0.46707193515704154,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 2.5 and cancel_cnt <= 1.5 and bidding_cnt <= 0.5 and industry_dx_rate > 0.0984530001879 and trade_mark_cnt <= 1.5 and network_share_cancel_cnt > 0.5",
    "sample_number": 987,
    "label": 1
  },
  {
    "missclassfication_rate": 0.22431557256402709,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years > 12.5 and judgedoc_cnt > 0.5 and cancel_cnt > 0.5 and trade_mark_cnt <= 2.5 and judgedoc_cnt <= 7.5",
    "sample_number": 3397,
    "label": 1
  },
  {
    "missclassfication_rate": 0.45979381443298967,
    "decision_path": "regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years > 12.5 and cancel_cnt > 0.5 and trade_mark_cnt <= 2.5 and judgedoc_cnt > 7.5",
    "sample_number": 485,
    "label": 1
  },
  {
    "missclassfication_rate": 0.4446210916799152,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years <= 12.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt <= 0.5 and trade_mark_cnt > 2.5 and trade_mark_cnt <= 5.5",
    "sample_number": 1887,
    "label": 0
  },
  {
    "missclassfication_rate": 0.25413223140495866,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years <= 12.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt <= 0.5 and trade_mark_cnt > 5.5",
    "sample_number": 968,
    "label": 0
  },
  {
    "missclassfication_rate": 0.46866333887964501,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years <= 12.5 and network_share_cancel_cnt > 0.5 and judgedoc_cnt > 0.5 and cancel_cnt <= 1.5",
    "sample_number": 1803,
    "label": 1
  },
  {
    "missclassfication_rate": 0.26666666666666666,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years <= 12.5 and network_share_cancel_cnt > 0.5 and judgedoc_cnt > 0.5 and cancel_cnt > 1.5",
    "sample_number": 810,
    "label": 1
  },
  {
    "missclassfication_rate": 0.31525423728813562,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 2.5 and cancel_cnt > 1.5 and bidding_cnt <= 0.5 and industry_dx_rate > 0.107982501388",
    "sample_number": 590,
    "label": 1
  },
  {
    "missclassfication_rate": 0.14066547120940426,
    "decision_path": "established_years <= 6.5 and established_years > 5.5 and address_change_cnt <= 0.5 and network_share_cancel_cnt <= 0.5 and regcap_change_cnt <= 0.5 and industry_dx_cnt <= 733.0",
    "sample_number": 5019,
    "label": 0
  },
  {
    "missclassfication_rate": 0.229430621279194,
    "decision_path": "established_years <= 6.5 and established_years > 5.5 and address_change_cnt <= 0.5 and network_share_cancel_cnt <= 0.5 and regcap_change_cnt <= 0.5 and industry_dx_cnt > 733.0",
    "sample_number": 6551,
    "label": 0
  },
  {
    "missclassfication_rate": 0.13455328310010764,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and established_years <= 16.5 and address_change_cnt <= 0.5 and judgedoc_cnt > 0.5 and network_share_cancel_cnt <= 0.5",
    "sample_number": 1858,
    "label": 0
  },
  {
    "missclassfication_rate": 0.33921302578018997,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and established_years <= 16.5 and address_change_cnt <= 0.5 and judgedoc_cnt > 0.5 and network_share_cancel_cnt > 0.5",
    "sample_number": 737,
    "label": 0
  },
  {
    "missclassfication_rate": 0.34408376963350784,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and network_share_cancel_cnt <= 0.5 and established_years <= 11.5 and address_change_cnt <= 1.5 and judgedoc_cnt <= 0.5",
    "sample_number": 4775,
    "label": 0
  },
  {
    "missclassfication_rate": 0.15450643776824036,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt > 0.5 and network_share_cancel_cnt <= 0.5 and established_years <= 11.5 and address_change_cnt <= 1.5 and judgedoc_cnt > 0.5",
    "sample_number": 699,
    "label": 0
  },
  {
    "missclassfication_rate": 0.14409937888198757,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt > 0.5 and cancel_cnt <= 0.5 and regcap_change_cnt <= 0.5",
    "sample_number": 6440,
    "label": 0
  },
  {
    "missclassfication_rate": 0.056782334384858045,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt > 0.5 and cancel_cnt <= 0.5 and regcap_change_cnt > 0.5",
    "sample_number": 5072,
    "label": 0
  },
  {
    "missclassfication_rate": 0.26784400294334071,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years <= 12.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt > 0.5 and cancel_cnt <= 0.5",
    "sample_number": 2718,
    "label": 0
  },
  {
    "missclassfication_rate": 0.48114901256732495,
    "decision_path": "established_years > 8.5 and regcap_change_cnt <= 0.5 and address_change_cnt <= 0.5 and established_years <= 12.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt > 0.5 and cancel_cnt > 0.5",
    "sample_number": 557,
    "label": 0
  },
  {
    "missclassfication_rate": 0.34165390505359877,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and regcap_change_cnt <= 0.5 and network_share_cancel_cnt <= 0.5 and trade_mark_cnt <= 2.5 and industry_dx_rate <= 0.0528304986656 and judgedoc_cnt <= 0.5",
    "sample_number": 6530,
    "label": 0
  },
  {
    "missclassfication_rate": 0.18343815513626835,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and regcap_change_cnt <= 0.5 and network_share_cancel_cnt <= 0.5 and trade_mark_cnt <= 2.5 and industry_dx_rate <= 0.0528304986656 and judgedoc_cnt > 0.5",
    "sample_number": 954,
    "label": 0
  },
  {
    "missclassfication_rate": 0.42233278054173579,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and established_years <= 16.5 and address_change_cnt > 0.5 and industry_dx_rate > 0.10734000057 and trade_mark_cnt <= 1.5",
    "sample_number": 1809,
    "label": 0
  },
  {
    "missclassfication_rate": 0.18509615384615385,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 0.5 and regcap_change_cnt <= 2.5 and cancel_cnt <= 0.5 and established_years <= 16.5 and address_change_cnt > 0.5 and industry_dx_rate > 0.10734000057 and trade_mark_cnt > 1.5",
    "sample_number": 416,
    "label": 0
  },
  {
    "missclassfication_rate": 0.45437788018433178,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 2.5 and cancel_cnt > 1.5 and bidding_cnt <= 0.5 and industry_dx_rate <= 0.107982501388 and judgedoc_cnt <= 0.5",
    "sample_number": 1085,
    "label": 1
  },
  {
    "missclassfication_rate": 0.34409937888198761,
    "decision_path": "established_years > 8.5 and regcap_change_cnt > 2.5 and cancel_cnt > 1.5 and bidding_cnt <= 0.5 and industry_dx_rate <= 0.107982501388 and judgedoc_cnt > 0.5",
    "sample_number": 805,
    "label": 0
  },
  {
    "missclassfication_rate": 0.19363574813811782,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and regcap_change_cnt > 0.5 and network_share_cancel_cnt <= 1.5 and industry_dx_rate <= 0.155301004648 and regcap_change_cnt <= 2.5",
    "sample_number": 7385,
    "label": 0
  },
  {
    "missclassfication_rate": 0.071428571428571425,
    "decision_path": "established_years <= 8.5 and established_years > 6.5 and address_change_cnt <= 0.5 and network_share_cancel_cnt <= 1.5 and industry_dx_rate <= 0.155301004648 and regcap_change_cnt > 2.5",
    "sample_number": 1456,
    "label": 0
  }
]

Process finished with exit code 0
