#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 
@site: 
@software: PyCharm
@file: dx_risk_rules_transfer.py
@time: 18-5-28 上午10:02
"""
import traceback

from src.decision_tree.feature_helper import FeatureHelper

dx_risk_rules = [
    {
        "missclassfication_rate": 0.38095238095238093,
        "decision_path": "court_notice_is_no > 0.5 and regcap <= 6.0",
        "sample_number": 21,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and judgedoc_cnt > 24.5",
        "sample_number": 9,
        "label": 0
    },
    {
        "missclassfication_rate": 0.3125,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and industry_dx_rate > 0.135145500302",
        "sample_number": 64,
        "label": 0
    },
    {
        "missclassfication_rate": 0.125,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt > 0.5",
        "sample_number": 8,
        "label": 0
    },
    {
        "missclassfication_rate": 0.25,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 13.5 and regcap <= 30.4500007629 and zczjbz <= 0.5",
        "sample_number": 12,
        "label": 0
    },
    {
        "missclassfication_rate": 0.14285714285714285,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no > 0.5 and judgedoc_cnt <= 1.5",
        "sample_number": 7,
        "label": 1
    },
    {
        "missclassfication_rate": 0.125,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and industry_dx_rate <= 0.135145500302 and net_judgedoc_defendant_cnt > 0.5 and shixin_cnt <= 2.5",
        "sample_number": 72,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and industry_dx_rate <= 0.135145500302 and net_judgedoc_defendant_cnt > 0.5 and shixin_cnt > 2.5",
        "sample_number": 7,
        "label": 0
    },
    {
        "missclassfication_rate": 0.23809523809523808,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt > 0.5 and regcap > 5925.07519531",
        "sample_number": 21,
        "label": 0
    },
    {
        "missclassfication_rate": 0.42105263157894735,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz <= 0.5",
        "sample_number": 19,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 5.5 and hy_shixin_cnt > 5.0",
        "sample_number": 3,
        "label": 0
    },
    {
        "missclassfication_rate": 0.36363636363636365,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt > 3.5",
        "sample_number": 11,
        "label": 0
    },
    {
        "missclassfication_rate": 0.16666666666666666,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years <= 18.5 and regcap <= 1408.2800293 and industry_all_cnt > 110011.0",
        "sample_number": 18,
        "label": 0
    },
    {
        "missclassfication_rate": 0.48484848484848486,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and industry_dx_rate <= 0.135145500302 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt > 0.5",
        "sample_number": 66,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years <= 4.5 and judgedoc_cnt > 14.5",
        "sample_number": 3,
        "label": 0
    },
    {
        "missclassfication_rate": 0.31481481481481483,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and industry_dx_rate <= 0.135145500302 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt > 0.5 and address_change_cnt > 1.5",
        "sample_number": 54,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and judgedoc_cnt <= 24.5 and litigant_result_sum_money <= -6577273.0",
        "sample_number": 3,
        "label": 0
    },
    {
        "missclassfication_rate": 0.15094339622641509,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and regcap > 30.4500007629 and established_years > 23.5 and industry_dx_rate > 0.0839914977551",
        "sample_number": 53,
        "label": 0
    },
    {
        "missclassfication_rate": 0.25,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_cnt > 3.0",
        "sample_number": 4,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years <= 18.5 and regcap > 1408.2800293 and network_share_zhixing_cnt > 1.5",
        "sample_number": 17,
        "label": 0
    },
    {
        "missclassfication_rate": 0.41791044776119401,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt > 10098.5 and share_change_cnt > 6.5",
        "sample_number": 67,
        "label": 0
    },
    {
        "missclassfication_rate": 0.44444444444444442,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no > 0.5 and judgedoc_cnt > 1.5 and network_fr_share_change_cnt > 5.5",
        "sample_number": 18,
        "label": 0
    },
    {
        "missclassfication_rate": 0.30769230769230771,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt > 8419.5",
        "sample_number": 26,
        "label": 1
    },
    {
        "missclassfication_rate": 0.15254237288135594,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and industry_dx_rate <= 0.135145500302 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_all_cnt > 32698.5",
        "sample_number": 59,
        "label": 1
    },
    {
        "missclassfication_rate": 0.18181818181818182,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 13.5 and established_years > 5.5 and regcap > 214.0 and industry_all_cnt <= 28963.5 and industry_dx_rate > 0.134651005268",
        "sample_number": 11,
        "label": 0
    },
    {
        "missclassfication_rate": 0.18181818181818182,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and industry_dx_rate <= 0.135145500302 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt > 0.5 and address_change_cnt <= 1.5 and zczjbz <= 0.5",
        "sample_number": 11,
        "label": 0
    },
    {
        "missclassfication_rate": 0.48484848484848486,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt > 0.5 and regcap <= 5925.07519531 and industry_all_cnt <= 5951.0",
        "sample_number": 33,
        "label": 0
    },
    {
        "missclassfication_rate": 0.22807017543859648,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt > 0.5 and regcap <= 5925.07519531 and industry_all_cnt > 5951.0",
        "sample_number": 57,
        "label": 1
    },
    {
        "missclassfication_rate": 0.42857142857142855,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and judgedoc_cnt <= 24.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt > 21.5",
        "sample_number": 21,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years <= 4.5 and judgedoc_cnt <= 14.5 and regcap_change_cnt > 2.5",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt <= 10098.5 and bidding_three_year_rate > 5.0",
        "sample_number": 2,
        "label": 1
    },
    {
        "missclassfication_rate": 0.25,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and judgedoc_cnt <= 24.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt > 0.5",
        "sample_number": 4,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and judgedoc_cnt <= 24.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt <= 0.5 and regcap <= 564.599975586",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 13.5 and regcap <= 30.4500007629 and zczjbz > 0.5 and industry_all_cnt > 38993.0 and regcap_change_cnt > 1.5",
        "sample_number": 3,
        "label": 0
    },
    {
        "missclassfication_rate": 0.125,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and regcap > 30.4500007629 and established_years > 23.5 and industry_dx_rate <= 0.0839914977551 and zczjbz <= 0.5",
        "sample_number": 16,
        "label": 0
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and regcap > 30.4500007629 and established_years > 23.5 and industry_dx_rate <= 0.0839914977551 and zczjbz > 0.5 and fr_change_cnt <= 3.5",
        "sample_number": 74,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and regcap > 30.4500007629 and established_years > 23.5 and industry_dx_rate <= 0.0839914977551 and zczjbz > 0.5 and fr_change_cnt > 3.5",
        "sample_number": 8,
        "label": 0
    },
    {
        "missclassfication_rate": 0.16666666666666666,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and industry_dx_rate <= 0.135145500302 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_all_cnt <= 32698.5 and regcap_change_cnt > 3.5",
        "sample_number": 6,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt > 2.0",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 13.5 and established_years > 5.5 and regcap > 214.0 and industry_all_cnt > 28963.5 and network_share_zhixing_cnt > 23.5",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and industry_dx_rate <= 0.135145500302 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_all_cnt <= 32698.5 and regcap_change_cnt <= 3.5 and industry_all_cnt > 31565.5",
        "sample_number": 3,
        "label": 0
    },
    {
        "missclassfication_rate": 0.26666666666666666,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years <= 18.5 and regcap > 1408.2800293 and network_share_zhixing_cnt <= 1.5 and regcap_change_cnt > 1.5",
        "sample_number": 75,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years <= 18.5 and network_share_zhixing_cnt <= 1.5 and regcap_change_cnt <= 1.5 and regcap > 18559.0",
        "sample_number": 9,
        "label": 0
    },
    {
        "missclassfication_rate": 0.30769230769230771,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and industry_dx_rate <= 0.135145500302 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt > 0.5 and address_change_cnt <= 1.5 and zczjbz > 0.5 and industry_dx_rate > 0.100308999419",
        "sample_number": 13,
        "label": 0
    },
    {
        "missclassfication_rate": 0.47272727272727272,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt > 0.5 and address_change_cnt <= 1.5 and zczjbz > 0.5 and industry_dx_rate <= 0.100308999419 and industry_dx_cnt <= 1571.0",
        "sample_number": 55,
        "label": 1
    },
    {
        "missclassfication_rate": 0.15625,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt > 0.5 and address_change_cnt <= 1.5 and zczjbz > 0.5 and industry_dx_rate <= 0.100308999419 and industry_dx_cnt > 1571.0",
        "sample_number": 32,
        "label": 1
    },
    {
        "missclassfication_rate": 0.40909090909090912,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years <= 18.5 and regcap > 1408.2800293 and network_share_zhixing_cnt <= 1.5 and regcap_change_cnt <= 1.5 and regcap <= 18559.0 and address_change_cnt <= 0.5",
        "sample_number": 66,
        "label": 0
    },
    {
        "missclassfication_rate": 0.33333333333333331,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years <= 18.5 and regcap > 1408.2800293 and network_share_zhixing_cnt <= 1.5 and regcap_change_cnt <= 1.5 and regcap <= 18559.0 and address_change_cnt > 0.5",
        "sample_number": 27,
        "label": 1
    },
    {
        "missclassfication_rate": 0.15789473684210525,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 13.5 and established_years > 5.5 and regcap > 214.0 and industry_all_cnt <= 28963.5 and industry_dx_rate <= 0.134651005268 and trademark_three_year_rate > 0.165000006557",
        "sample_number": 19,
        "label": 1
    },
    {
        "missclassfication_rate": 0.40000000000000002,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 30.4500007629 and zczjbz > 0.5 and industry_all_cnt <= 38993.0 and established_years > 30.5",
        "sample_number": 5,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt > 10098.5 and share_change_cnt <= 6.5 and invent_publish_three_year_rate > 0.5",
        "sample_number": 2,
        "label": 1
    },
    {
        "missclassfication_rate": 0.40625,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and fr_change_cnt > 1.5",
        "sample_number": 32,
        "label": 1
    },
    {
        "missclassfication_rate": 0.33333333333333331,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt > 1.5",
        "sample_number": 3,
        "label": 0
    },
    {
        "missclassfication_rate": 0.1875,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 5.5 and regcap > 214.0 and industry_all_cnt <= 28963.5 and industry_dx_rate <= 0.134651005268 and trademark_three_year_rate <= 0.165000006557 and established_years <= 6.5",
        "sample_number": 16,
        "label": 1
    },
    {
        "missclassfication_rate": 0.23529411764705882,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 13.5 and regcap > 214.0 and industry_all_cnt <= 28963.5 and industry_dx_rate <= 0.134651005268 and trademark_three_year_rate <= 0.165000006557 and established_years > 6.5 and industry_all_cnt > 13549.0",
        "sample_number": 17,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and established_years <= 23.5 and industry_dx_rate <= 0.135145500302 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and regcap_change_cnt <= 3.5 and industry_all_cnt <= 31565.5 and trade_mark_cnt > 0.5",
        "sample_number": 10,
        "label": 1
    },
    {
        "missclassfication_rate": 0.16666666666666666,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and regcap > 30.4500007629 and established_years <= 23.5 and industry_dx_rate <= 0.135145500302 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and regcap_change_cnt <= 3.5 and industry_all_cnt <= 31565.5 and trade_mark_cnt <= 0.5 and established_years > 22.5",
        "sample_number": 6,
        "label": 0
    },
    {
        "missclassfication_rate": 0.44444444444444442,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt > 10098.5 and share_change_cnt <= 6.5 and invent_publish_three_year_rate <= 0.5 and bidding_cnt > 1.5",
        "sample_number": 9,
        "label": 1
    },
    {
        "missclassfication_rate": 0.026315789473684209,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt > 10098.5 and share_change_cnt <= 6.5 and invent_publish_three_year_rate <= 0.5 and bidding_cnt <= 1.5 and regcap > 5009.0",
        "sample_number": 38,
        "label": 0
    },
    {
        "missclassfication_rate": 0.41379310344827586,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt > 10098.5 and share_change_cnt <= 6.5 and invent_publish_three_year_rate <= 0.5 and bidding_cnt <= 1.5 and regcap <= 5009.0 and industry_dx_rate > 0.108205005527",
        "sample_number": 29,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and fr_change_cnt <= 1.5 and network_share_cancel_cnt > 0.5 and industry_1810 > 0.5",
        "sample_number": 3,
        "label": 0
    },
    {
        "missclassfication_rate": 0.29166666666666669,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and fr_change_cnt <= 1.5 and network_share_cancel_cnt > 0.5 and industry_1810 <= 0.5 and network_fr_share_change_cnt <= 0.5",
        "sample_number": 72,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0625,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and fr_change_cnt <= 1.5 and network_share_cancel_cnt > 0.5 and industry_1810 <= 0.5 and network_fr_share_change_cnt > 0.5",
        "sample_number": 32,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 13.5 and regcap <= 30.4500007629 and zczjbz > 0.5 and industry_all_cnt > 38993.0 and regcap_change_cnt <= 1.5 and bidding_three_year_rate > 0.335000008345",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.20000000000000001,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt <= 4518.0 and industry_all_cnt > 4398.5",
        "sample_number": 5,
        "label": 0
    },
    {
        "missclassfication_rate": 0.071428571428571425,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt <= 4398.5 and established_years <= 6.5",
        "sample_number": 14,
        "label": 1
    },
    {
        "missclassfication_rate": 0.37333333333333335,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt <= 4398.5 and established_years > 6.5",
        "sample_number": 75,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate > 0.165000006557",
        "sample_number": 4,
        "label": 1
    },
    {
        "missclassfication_rate": 0.26000000000000001,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt > 3.5 and industry_all_cnt > 31827.5",
        "sample_number": 50,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt > 3.5 and industry_all_cnt <= 31827.5 and punish_cnt > 0.5",
        "sample_number": 2,
        "label": 1
    },
    {
        "missclassfication_rate": 0.4375,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years <= 18.5 and regcap <= 1408.2800293 and industry_all_cnt <= 8201.5 and regcap_change_cnt <= 0.5",
        "sample_number": 32,
        "label": 1
    },
    {
        "missclassfication_rate": 0.33333333333333331,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years <= 18.5 and regcap <= 1408.2800293 and industry_all_cnt <= 8201.5 and regcap_change_cnt > 0.5",
        "sample_number": 51,
        "label": 0
    },
    {
        "missclassfication_rate": 0.27500000000000002,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and fr_change_cnt <= 1.5 and network_share_cancel_cnt <= 0.5 and fr_change_cnt > 0.5",
        "sample_number": 40,
        "label": 1
    },
    {
        "missclassfication_rate": 0.28888888888888886,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and judgedoc_cnt <= 24.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt <= 0.5 and regcap > 564.599975586 and industry_all_cnt <= 34061.5 and network_share_cancel_cnt > 0.5",
        "sample_number": 45,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years <= 18.5 and regcap <= 1408.2800293 and industry_all_cnt <= 110011.0 and industry_all_cnt > 8201.5 and zhixing_cnt > 2.0",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt > 0.5 and regcap_change_cnt > 3.5",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt > 2.5",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt > 31.0",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt <= 3.5 and industry_26 > 0.5",
        "sample_number": 1,
        "label": 1
    },
    {
        "missclassfication_rate": 0.32142857142857145,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 13.5 and established_years > 5.5 and regcap > 214.0 and industry_all_cnt > 28963.5 and network_share_zhixing_cnt <= 23.5 and industry_dx_cnt > 6893.0",
        "sample_number": 28,
        "label": 1
    },
    {
        "missclassfication_rate": 0.3728813559322034,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years <= 18.5 and regcap <= 1408.2800293 and industry_all_cnt > 8201.5 and zhixing_cnt <= 2.0 and industry_all_cnt <= 55396.5",
        "sample_number": 59,
        "label": 1
    },
    {
        "missclassfication_rate": 0.15384615384615385,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years <= 18.5 and regcap <= 1408.2800293 and industry_all_cnt <= 110011.0 and zhixing_cnt <= 2.0 and industry_all_cnt > 55396.5",
        "sample_number": 26,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 13.5 and regcap <= 30.4500007629 and zczjbz > 0.5 and industry_all_cnt <= 38993.0 and established_years <= 30.5 and industry_dx_cnt > 3511.0",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 13.5 and regcap <= 30.4500007629 and zczjbz > 0.5 and industry_all_cnt <= 38993.0 and established_years <= 30.5 and industry_dx_cnt <= 3511.0 and share_change_cnt > 17.0",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no > 0.5 and judgedoc_cnt > 1.5 and network_fr_share_change_cnt <= 5.5 and bidding_three_year_rate > 4.17000007629",
        "sample_number": 1,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no > 0.5 and judgedoc_cnt > 1.5 and network_fr_share_change_cnt <= 5.5 and bidding_three_year_rate <= 4.17000007629 and court_announce_cnt > 74.0",
        "sample_number": 1,
        "label": 1
    },
    {
        "missclassfication_rate": 0.19444444444444445,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no > 0.5 and judgedoc_cnt > 1.5 and network_fr_share_change_cnt <= 5.5 and bidding_three_year_rate <= 4.17000007629 and court_announce_cnt <= 74.0 and shixin_cnt <= 2.5",
        "sample_number": 36,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no > 0.5 and judgedoc_cnt > 1.5 and network_fr_share_change_cnt <= 5.5 and bidding_three_year_rate <= 4.17000007629 and court_announce_cnt <= 74.0 and shixin_cnt > 2.5",
        "sample_number": 59,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years <= 4.5 and judgedoc_cnt <= 14.5 and regcap_change_cnt <= 2.5 and litigant_defendant_Intellectual_property_owner_cnt > 0.5",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.19298245614035087,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years <= 4.5 and judgedoc_cnt <= 14.5 and regcap_change_cnt <= 2.5 and litigant_defendant_Intellectual_property_owner_cnt <= 0.5 and established_years > 3.5",
        "sample_number": 57,
        "label": 1
    },
    {
        "missclassfication_rate": 0.013157894736842105,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and judgedoc_cnt <= 14.5 and regcap_change_cnt <= 2.5 and litigant_defendant_Intellectual_property_owner_cnt <= 0.5 and established_years <= 3.5 and network_fr_share_change_cnt <= 7.0",
        "sample_number": 76,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and judgedoc_cnt <= 14.5 and regcap_change_cnt <= 2.5 and litigant_defendant_Intellectual_property_owner_cnt <= 0.5 and established_years <= 3.5 and network_fr_share_change_cnt > 7.0",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.34615384615384615,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt > 10098.5 and share_change_cnt <= 6.5 and invent_publish_three_year_rate <= 0.5 and bidding_cnt <= 1.5 and industry_dx_rate <= 0.108205005527 and regcap <= 956.0",
        "sample_number": 26,
        "label": 0
    },
    {
        "missclassfication_rate": 0.44444444444444442,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt > 10098.5 and share_change_cnt <= 6.5 and invent_publish_three_year_rate <= 0.5 and bidding_cnt <= 1.5 and regcap <= 5009.0 and industry_dx_rate <= 0.108205005527 and regcap > 956.0 and established_years <= 6.5",
        "sample_number": 9,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and judgedoc_cnt <= 24.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt <= 0.5 and regcap > 564.599975586 and industry_all_cnt <= 34061.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt > 16.5",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt <= 0.5 and regcap > 564.599975586 and industry_all_cnt <= 34061.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt <= 16.5 and hy_shixin_cnt > 5.5",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt <= 0.5 and regcap > 564.599975586 and industry_all_cnt <= 34061.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt <= 16.5 and hy_shixin_cnt <= 5.5 and cancel_cnt > 20.5",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 13.5 and established_years > 5.5 and regcap > 214.0 and industry_all_cnt > 28963.5 and network_share_zhixing_cnt <= 23.5 and industry_dx_cnt <= 6893.0 and near_2_year_shixin_cnt > 3.0",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.092105263157894732,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 13.5 and established_years > 5.5 and regcap > 214.0 and industry_all_cnt > 28963.5 and network_share_zhixing_cnt <= 23.5 and industry_dx_cnt <= 6893.0 and near_2_year_shixin_cnt <= 3.0 and cancel_cnt <= 3.5",
        "sample_number": 76,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 13.5 and established_years > 5.5 and regcap > 214.0 and industry_all_cnt > 28963.5 and network_share_zhixing_cnt <= 23.5 and industry_dx_cnt <= 6893.0 and near_2_year_shixin_cnt <= 3.0 and cancel_cnt > 3.5",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt > 10098.5 and share_change_cnt <= 6.5 and invent_publish_three_year_rate <= 0.5 and bidding_cnt <= 1.5 and regcap <= 5009.0 and industry_dx_rate <= 0.108205005527 and regcap > 956.0 and established_years > 6.5 and fine_cnt > 0.5",
        "sample_number": 1,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap <= 19.0 and bidding_three_year_rate > 0.665000021458",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap <= 19.0 and bidding_three_year_rate <= 0.665000021458 and punish_cnt > 1.0",
        "sample_number": 1,
        "label": 0
    },
    {
        "missclassfication_rate": 0.35714285714285715,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap > 209.0 and industry_all_cnt > 60833.5",
        "sample_number": 14,
        "label": 1
    },
    {
        "missclassfication_rate": 0.375,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt <= 0.5 and regcap > 564.599975586 and industry_all_cnt <= 34061.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt <= 16.5 and hy_shixin_cnt <= 5.5 and cancel_cnt <= 20.5 and industry_dx_cnt > 1900.0",
        "sample_number": 8,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years > 58.0",
        "sample_number": 1,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years > 18.5 and established_years <= 58.0 and regcap > 72999.484375",
        "sample_number": 1,
        "label": 1
    },
    {
        "missclassfication_rate": 0.48684210526315791,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 13.5 and regcap > 214.0 and industry_dx_rate <= 0.134651005268 and trademark_three_year_rate <= 0.165000006557 and established_years > 6.5 and industry_all_cnt <= 13549.0 and near_1_year_judgedoc_cnt <= 3.5",
        "sample_number": 76,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 13.5 and regcap > 214.0 and industry_dx_rate <= 0.134651005268 and trademark_three_year_rate <= 0.165000006557 and established_years > 6.5 and industry_all_cnt <= 13549.0 and near_1_year_judgedoc_cnt > 3.5",
        "sample_number": 3,
        "label": 0
    },
    {
        "missclassfication_rate": 0.22535211267605634,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 13.5 and regcap <= 30.4500007629 and zczjbz > 0.5 and industry_all_cnt > 38993.0 and regcap_change_cnt <= 1.5 and bidding_three_year_rate <= 0.335000008345 and share_change_cnt <= 0.5",
        "sample_number": 71,
        "label": 1
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 13.5 and regcap <= 30.4500007629 and zczjbz > 0.5 and industry_all_cnt > 38993.0 and regcap_change_cnt <= 1.5 and bidding_three_year_rate <= 0.335000008345 and share_change_cnt > 0.5",
        "sample_number": 10,
        "label": 0
    },
    {
        "missclassfication_rate": 0.40000000000000002,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt <= 0.5 and regcap > 564.599975586 and industry_all_cnt <= 34061.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt <= 16.5 and hy_shixin_cnt <= 5.5 and cancel_cnt <= 20.5 and industry_dx_cnt <= 1900.0 and regcap_change_cnt > 9.0",
        "sample_number": 5,
        "label": 1
    },
    {
        "missclassfication_rate": 0.33333333333333331,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt <= 10098.5 and bidding_three_year_rate <= 5.0 and regcap <= 3290.0 and regcap > 3211.79003906",
        "sample_number": 3,
        "label": 1
    },
    {
        "missclassfication_rate": 0.20689655172413793,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years > 18.5 and regcap <= 72999.484375 and established_years <= 24.5",
        "sample_number": 58,
        "label": 0
    },
    {
        "missclassfication_rate": 0.057692307692307696,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and established_years <= 58.0 and regcap <= 72999.484375 and established_years > 24.5",
        "sample_number": 52,
        "label": 0
    },
    {
        "missclassfication_rate": 0.18181818181818182,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and industry_dx_rate <= 0.135145500302 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and regcap_change_cnt <= 3.5 and industry_all_cnt <= 31565.5 and trade_mark_cnt <= 0.5 and established_years <= 22.5 and industry_dx_rate > 0.0872910022736",
        "sample_number": 22,
        "label": 1
    },
    {
        "missclassfication_rate": 0.20000000000000001,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and regcap_change_cnt <= 3.5 and industry_all_cnt <= 31565.5 and trade_mark_cnt <= 0.5 and established_years <= 22.5 and industry_dx_rate <= 0.0872910022736 and industry_dx_rate > 0.0846344977617",
        "sample_number": 5,
        "label": 0
    },
    {
        "missclassfication_rate": 0.36486486486486486,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and regcap_change_cnt <= 3.5 and industry_all_cnt <= 31565.5 and trade_mark_cnt <= 0.5 and established_years <= 22.5 and industry_dx_rate <= 0.080210506916",
        "sample_number": 74,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years > 13.5 and regcap > 30.4500007629 and net_judgedoc_defendant_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and regcap_change_cnt <= 3.5 and industry_all_cnt <= 31565.5 and trade_mark_cnt <= 0.5 and established_years <= 22.5 and industry_dx_rate <= 0.0846344977617 and industry_dx_rate > 0.080210506916",
        "sample_number": 6,
        "label": 1
    },
    {
        "missclassfication_rate": 0.067796610169491525,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt <= 10098.5 and bidding_three_year_rate <= 5.0 and regcap <= 3211.79003906 and network_fr_share_change_cnt <= 0.5",
        "sample_number": 59,
        "label": 0
    },
    {
        "missclassfication_rate": 0.20000000000000001,
        "decision_path": "court_notice_is_no <= 0.5 and regcap > 521.145019531 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt <= 10098.5 and bidding_three_year_rate <= 5.0 and regcap <= 3211.79003906 and network_fr_share_change_cnt > 0.5",
        "sample_number": 75,
        "label": 0
    },
    {
        "missclassfication_rate": 0.20000000000000001,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 13.5 and regcap <= 30.4500007629 and zczjbz > 0.5 and industry_all_cnt <= 38993.0 and established_years <= 30.5 and industry_dx_cnt <= 3511.0 and share_change_cnt <= 17.0 and address_change_cnt > 1.5",
        "sample_number": 25,
        "label": 1
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_cnt <= 3.0 and litigant_defendant_contract_dispute_cnt > 6.5",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.033898305084745763,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap <= 19.0 and bidding_three_year_rate <= 0.665000021458 and punish_cnt <= 1.0 and industry_dx_cnt <= 90.0",
        "sample_number": 59,
        "label": 1
    },
    {
        "missclassfication_rate": 0.20000000000000001,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap <= 19.0 and bidding_three_year_rate <= 0.665000021458 and punish_cnt <= 1.0 and industry_dx_cnt > 90.0 and industry_dx_cnt <= 107.5",
        "sample_number": 5,
        "label": 0
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap <= 19.0 and bidding_three_year_rate <= 0.665000021458 and punish_cnt <= 1.0 and industry_dx_cnt > 107.5 and regcap_change_cnt > 0.5",
        "sample_number": 4,
        "label": 0
    },
    {
        "missclassfication_rate": 0.25,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap <= 19.0 and bidding_three_year_rate <= 0.665000021458 and punish_cnt <= 1.0 and industry_dx_cnt > 107.5 and regcap_change_cnt <= 0.5 and share_change_cnt > 0.5",
        "sample_number": 20,
        "label": 1
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt > 3.5 and industry_all_cnt <= 31827.5 and punish_cnt <= 0.5 and established_years <= 5.5",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.026666666666666668,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt > 3.5 and industry_all_cnt <= 31827.5 and punish_cnt <= 0.5 and established_years > 5.5",
        "sample_number": 75,
        "label": 0
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt <= 3.5 and industry_26 <= 0.5 and litigant_defendant_contract_dispute_cnt > 106.0",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.25,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap > 209.0 and industry_all_cnt <= 60833.5 and fr_change_cnt > 0.5",
        "sample_number": 12,
        "label": 1
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt <= 10098.5 and bidding_three_year_rate <= 5.0 and regcap > 202537.53125",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap > 209.0 and industry_all_cnt <= 60833.5 and fr_change_cnt <= 0.5 and regcap <= 214.0",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and judgedoc_cnt <= 24.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt <= 0.5 and regcap > 564.599975586 and industry_all_cnt > 34061.5 and court_announce_is_no <= 0.5",
        "sample_number": 69,
        "label": 1
    },
    {
        "missclassfication_rate": 0.14999999999999999,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and judgedoc_cnt <= 24.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt <= 0.5 and regcap > 564.599975586 and industry_all_cnt > 34061.5 and court_announce_is_no > 0.5",
        "sample_number": 20,
        "label": 1
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap <= 19.0 and bidding_three_year_rate <= 0.665000021458 and punish_cnt <= 1.0 and industry_dx_cnt > 107.5 and regcap_change_cnt <= 0.5 and share_change_cnt <= 0.5 and fr_change_cnt > 4.5",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap <= 19.0 and bidding_three_year_rate <= 0.665000021458 and punish_cnt <= 1.0 and industry_dx_cnt > 107.5 and regcap_change_cnt <= 0.5 and share_change_cnt <= 0.5 and fr_change_cnt <= 4.5 and industry_519 > 0.5",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.40000000000000002,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt <= 3.5 and industry_26 <= 0.5 and litigant_defendant_contract_dispute_cnt <= 106.0 and judge_doc_cnt <= 3.5 and established_years <= 13.5 and near_1_year_judgedoc_cnt > 11.0",
        "sample_number": 5,
        "label": 0
    },
    {
        "missclassfication_rate": 0.16666666666666666,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt <= 3.5 and industry_26 <= 0.5 and litigant_defendant_contract_dispute_cnt <= 106.0 and judge_doc_cnt <= 3.5 and established_years <= 13.5 and near_1_year_judgedoc_cnt <= 11.0 and industry_dx_rate <= 0.0710445046425",
        "sample_number": 42,
        "label": 0
    },
    {
        "missclassfication_rate": 0.022727272727272728,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt <= 3.5 and industry_26 <= 0.5 and litigant_defendant_contract_dispute_cnt <= 106.0 and judge_doc_cnt <= 3.5 and established_years <= 13.5 and near_1_year_judgedoc_cnt <= 11.0 and industry_dx_rate > 0.0710445046425",
        "sample_number": 44,
        "label": 0
    },
    {
        "missclassfication_rate": 0.013157894736842105,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 13.5 and regcap <= 30.4500007629 and zczjbz > 0.5 and industry_all_cnt <= 38993.0 and industry_dx_cnt <= 3511.0 and share_change_cnt <= 17.0 and address_change_cnt <= 1.5 and established_years <= 20.5",
        "sample_number": 76,
        "label": 1
    },
    {
        "missclassfication_rate": 0.15789473684210525,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 30.4500007629 and zczjbz > 0.5 and industry_all_cnt <= 38993.0 and established_years <= 30.5 and industry_dx_cnt <= 3511.0 and share_change_cnt <= 17.0 and address_change_cnt <= 1.5 and established_years > 20.5",
        "sample_number": 19,
        "label": 1
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no <= 0.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt > 10098.5 and share_change_cnt <= 6.5 and invent_publish_three_year_rate <= 0.5 and bidding_cnt <= 1.5 and regcap <= 5009.0 and industry_dx_rate <= 0.108205005527 and regcap > 956.0 and established_years > 6.5 and fine_cnt <= 0.5 and industry_all_cnt <= 10765.0",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.33333333333333331,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt > 1.5 and established_years > 46.0",
        "sample_number": 3,
        "label": 0
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and network_share_cancel_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt > 0.5",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.33333333333333331,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap <= 209.0 and zczjbz <= 0.5",
        "sample_number": 3,
        "label": 1
    },
    {
        "missclassfication_rate": 0.33333333333333331,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt <= 0.5 and regcap > 564.599975586 and industry_all_cnt <= 34061.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt <= 16.5 and hy_shixin_cnt <= 5.5 and cancel_cnt <= 20.5 and industry_dx_cnt <= 1900.0 and regcap_change_cnt <= 9.0 and cancel_cnt > 2.5",
        "sample_number": 3,
        "label": 1
    },
    {
        "missclassfication_rate": 0.13559322033898305,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and bidding_three_year_rate <= 0.665000021458 and punish_cnt <= 1.0 and industry_dx_cnt > 107.5 and regcap_change_cnt <= 0.5 and share_change_cnt <= 0.5 and fr_change_cnt <= 4.5 and industry_519 <= 0.5 and regcap <= 0.5",
        "sample_number": 59,
        "label": 1
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap <= 19.0 and bidding_three_year_rate <= 0.665000021458 and punish_cnt <= 1.0 and industry_dx_cnt > 107.5 and regcap_change_cnt <= 0.5 and share_change_cnt <= 0.5 and fr_change_cnt <= 4.5 and industry_519 <= 0.5 and regcap > 0.5 and fr_change_cnt > 0.5",
        "sample_number": 2,
        "label": 0
    },
    {
        "missclassfication_rate": 0.17857142857142858,
        "decision_path": "court_notice_is_no <= 0.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and share_change_cnt <= 6.5 and invent_publish_three_year_rate <= 0.5 and bidding_cnt <= 1.5 and regcap <= 5009.0 and industry_dx_rate <= 0.108205005527 and regcap > 956.0 and established_years > 6.5 and fine_cnt <= 0.5 and industry_all_cnt > 10765.0 and established_years <= 10.5",
        "sample_number": 28,
        "label": 0
    },
    {
        "missclassfication_rate": 0.065573770491803282,
        "decision_path": "court_notice_is_no <= 0.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and share_change_cnt <= 6.5 and invent_publish_three_year_rate <= 0.5 and bidding_cnt <= 1.5 and regcap <= 5009.0 and industry_dx_rate <= 0.108205005527 and regcap > 956.0 and fine_cnt <= 0.5 and industry_all_cnt > 10765.0 and established_years > 10.5",
        "sample_number": 61,
        "label": 0
    },
    {
        "missclassfication_rate": 0.028571428571428571,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and network_share_cancel_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_dx_rate <= 0.0404885001481",
        "sample_number": 35,
        "label": 1
    },
    {
        "missclassfication_rate": 0.27777777777777779,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and network_share_cancel_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_dx_rate > 0.0404885001481 and industry_dx_rate <= 0.0511165000498",
        "sample_number": 18,
        "label": 1
    },
    {
        "missclassfication_rate": 0.037735849056603772,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and network_share_cancel_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_dx_rate > 0.0511165000498 and industry_all_cnt > 61693.0",
        "sample_number": 53,
        "label": 1
    },
    {
        "missclassfication_rate": 0.25,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and industry_all_cnt > 4518.0 and network_share_cancel_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_dx_rate > 0.0511165000498 and industry_all_cnt <= 61693.0 and regcap > 160.449996948",
        "sample_number": 24,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and network_share_cancel_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_dx_rate > 0.0511165000498 and industry_all_cnt <= 61693.0 and regcap <= 160.449996948 and industry_dx_cnt <= 619.0",
        "sample_number": 30,
        "label": 1
    },
    {
        "missclassfication_rate": 0.5,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and network_share_cancel_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_dx_rate > 0.0511165000498 and industry_all_cnt <= 61693.0 and regcap <= 160.449996948 and industry_dx_cnt > 619.0 and industry_dx_cnt <= 707.0",
        "sample_number": 6,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and network_share_cancel_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_dx_rate > 0.0511165000498 and industry_all_cnt <= 61693.0 and regcap <= 160.449996948 and industry_dx_cnt > 707.0 and industry_dx_cnt <= 1290.0",
        "sample_number": 25,
        "label": 1
    },
    {
        "missclassfication_rate": 0.40000000000000002,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and network_share_cancel_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_dx_rate > 0.0511165000498 and industry_all_cnt <= 61693.0 and regcap <= 160.449996948 and industry_dx_cnt > 1290.0 and industry_dx_cnt <= 1457.5",
        "sample_number": 5,
        "label": 1
    },
    {
        "missclassfication_rate": 0.25,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt <= 3.5 and industry_26 <= 0.5 and litigant_defendant_contract_dispute_cnt <= 106.0 and judge_doc_cnt <= 3.5 and established_years > 36.5",
        "sample_number": 4,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and network_share_cancel_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_dx_rate > 0.0511165000498 and industry_all_cnt <= 61693.0 and regcap <= 160.449996948 and industry_dx_cnt > 1457.5 and established_years > 12.5",
        "sample_number": 12,
        "label": 1
    },
    {
        "missclassfication_rate": 0.10000000000000001,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and network_share_cancel_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_dx_rate > 0.0511165000498 and industry_all_cnt <= 61693.0 and regcap <= 160.449996948 and industry_dx_cnt > 1457.5 and established_years <= 12.5 and industry_dx_cnt <= 3879.5",
        "sample_number": 70,
        "label": 1
    },
    {
        "missclassfication_rate": 0.18604651162790697,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap > 19.0 and industry_all_cnt > 4518.0 and network_share_cancel_cnt <= 0.5 and fr_change_cnt <= 0.5 and cancel_cnt <= 0.5 and industry_dx_rate > 0.0511165000498 and industry_all_cnt <= 61693.0 and regcap <= 160.449996948 and established_years <= 12.5 and industry_dx_cnt > 3879.5",
        "sample_number": 43,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt > 0.5 and regcap_change_cnt <= 3.5 and industry_all_cnt > 17158.0",
        "sample_number": 107,
        "label": 1
    },
    {
        "missclassfication_rate": 0.029850746268656716,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt > 0.5 and regcap_change_cnt <= 3.5 and industry_all_cnt <= 17158.0 and industry_dx_cnt <= 1159.0",
        "sample_number": 67,
        "label": 1
    },
    {
        "missclassfication_rate": 0.29999999999999999,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt > 0.5 and regcap_change_cnt <= 3.5 and industry_all_cnt <= 17158.0 and industry_dx_cnt > 1159.0",
        "sample_number": 10,
        "label": 1
    },
    {
        "missclassfication_rate": 0.095238095238095233,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 5.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap <= 19.0 and bidding_three_year_rate <= 0.665000021458 and punish_cnt <= 1.0 and industry_dx_cnt > 107.5 and regcap_change_cnt <= 0.5 and share_change_cnt <= 0.5 and industry_519 <= 0.5 and regcap > 0.5 and fr_change_cnt <= 0.5 and established_years <= 7.5",
        "sample_number": 42,
        "label": 1
    },
    {
        "missclassfication_rate": 0.014705882352941176,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt <= 0.5 and network_share_sszc_cnt <= 2.0 and regcap <= 19.0 and bidding_three_year_rate <= 0.665000021458 and punish_cnt <= 1.0 and industry_dx_cnt > 107.5 and regcap_change_cnt <= 0.5 and share_change_cnt <= 0.5 and industry_519 <= 0.5 and regcap > 0.5 and fr_change_cnt <= 0.5 and established_years > 7.5",
        "sample_number": 68,
        "label": 1
    },
    {
        "missclassfication_rate": 0.081081081081081086,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt <= 10098.5 and bidding_three_year_rate <= 5.0 and regcap > 3290.0 and regcap <= 202537.53125 and address_change_cnt <= 0.5",
        "sample_number": 37,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt <= 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt > 0.5 and industry_all_cnt <= 10098.5 and bidding_three_year_rate <= 5.0 and regcap > 3290.0 and regcap <= 202537.53125 and address_change_cnt > 0.5",
        "sample_number": 49,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0625,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt > 1.5 and established_years <= 46.0 and regcap <= 102.5",
        "sample_number": 48,
        "label": 0
    },
    {
        "missclassfication_rate": 0.16666666666666666,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt <= 0.5 and regcap > 564.599975586 and industry_all_cnt <= 34061.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt <= 16.5 and hy_shixin_cnt <= 5.5 and industry_dx_cnt <= 1900.0 and regcap_change_cnt <= 9.0 and cancel_cnt <= 2.5 and regcap <= 940.0",
        "sample_number": 6,
        "label": 1
    },
    {
        "missclassfication_rate": 0.013333333333333334,
        "decision_path": "court_notice_is_no <= 0.5 and established_years > 4.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_is_no <= 0.5 and litigant_result_sum_money > -6577273.0 and zhixing_cnt <= 21.5 and litigant_defendant_bust_cnt <= 0.5 and industry_all_cnt <= 34061.5 and network_share_cancel_cnt <= 0.5 and judgedoc_cnt <= 16.5 and hy_shixin_cnt <= 5.5 and industry_dx_cnt <= 1900.0 and regcap_change_cnt <= 9.0 and cancel_cnt <= 2.5 and regcap > 940.0",
        "sample_number": 75,
        "label": 1
    },
    {
        "missclassfication_rate": 0.07407407407407407,
        "decision_path": "court_notice_is_no > 0.5 and near_3_year_judgedoc_cnt > 1.5 and established_years <= 46.0 and regcap > 102.5 and trademark_three_year_rate > 1.5",
        "sample_number": 27,
        "label": 0
    },
    {
        "missclassfication_rate": 0.068965517241379309,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and industry_all_cnt <= 60833.5 and fr_change_cnt <= 0.5 and regcap > 214.0 and industry_dx_cnt <= 1270.0",
        "sample_number": 58,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and regcap <= 521.145019531 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and industry_all_cnt <= 60833.5 and fr_change_cnt <= 0.5 and regcap > 214.0 and industry_dx_cnt > 1270.0",
        "sample_number": 43,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap <= 209.0 and zczjbz > 0.5 and trade_mark_cnt > 0.5",
        "sample_number": 237,
        "label": 1
    },
    {
        "missclassfication_rate": 0.25,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap <= 209.0 and zczjbz > 0.5 and trade_mark_cnt <= 0.5 and established_years > 4.5 and industry_dx_rate > 0.11021900177",
        "sample_number": 8,
        "label": 1
    },
    {
        "missclassfication_rate": 0.16666666666666666,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap <= 209.0 and zczjbz > 0.5 and trade_mark_cnt <= 0.5 and established_years > 4.5 and industry_dx_rate <= 0.11021900177 and industry_all_cnt <= 4796.0",
        "sample_number": 12,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_cnt <= 3.0 and litigant_defendant_contract_dispute_cnt <= 6.5 and industry_all_cnt <= 93008.5",
        "sample_number": 118,
        "label": 1
    },
    {
        "missclassfication_rate": 0.090909090909090912,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 13.5 and established_years > 5.5 and regcap <= 214.0 and estate_auction_cnt <= 0.5 and trade_mark_cnt <= 0.5 and zczjbz > 0.5 and address_change_cnt <= 3.5 and net_judgedoc_defendant_cnt > 0.5 and shixin_cnt <= 3.0 and litigant_defendant_contract_dispute_cnt <= 6.5 and industry_all_cnt > 93008.5",
        "sample_number": 11,
        "label": 1
    },
    {
        "missclassfication_rate": 0.10000000000000001,
        "decision_path": "court_notice_is_no <= 0.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap <= 209.0 and zczjbz > 0.5 and trade_mark_cnt <= 0.5 and established_years <= 4.5 and fr_change_cnt > 0.5",
        "sample_number": 10,
        "label": 1
    },
    {
        "missclassfication_rate": 0.052631578947368418,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt <= 3.5 and industry_26 <= 0.5 and litigant_defendant_contract_dispute_cnt <= 106.0 and judge_doc_cnt <= 3.5 and established_years > 13.5 and established_years <= 36.5 and industry_dx_cnt <= 487.0",
        "sample_number": 38,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt <= 3.5 and industry_26 <= 0.5 and litigant_defendant_contract_dispute_cnt <= 106.0 and judge_doc_cnt <= 3.5 and established_years > 13.5 and established_years <= 36.5 and industry_dx_cnt > 487.0",
        "sample_number": 83,
        "label": 0
    },
    {
        "missclassfication_rate": 0.058823529411764705,
        "decision_path": "court_notice_is_no > 0.5 and near_3_year_judgedoc_cnt > 1.5 and established_years <= 46.0 and regcap > 102.5 and trademark_three_year_rate <= 1.5 and industry_all_cnt > 78776.5 and hy_shixin_cnt <= 0.5",
        "sample_number": 68,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no > 0.5 and near_3_year_judgedoc_cnt > 1.5 and established_years <= 46.0 and regcap > 102.5 and trademark_three_year_rate <= 1.5 and industry_all_cnt > 78776.5 and hy_shixin_cnt > 0.5",
        "sample_number": 92,
        "label": 0
    },
    {
        "missclassfication_rate": 0.076923076923076927,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap <= 209.0 and zczjbz > 0.5 and trade_mark_cnt <= 0.5 and established_years > 4.5 and industry_dx_rate <= 0.11021900177 and industry_all_cnt > 4796.0 and industry_dx_cnt <= 448.5",
        "sample_number": 13,
        "label": 1
    },
    {
        "missclassfication_rate": 0.013513513513513514,
        "decision_path": "court_notice_is_no <= 0.5 and established_years <= 5.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap <= 209.0 and zczjbz > 0.5 and trade_mark_cnt <= 0.5 and established_years > 4.5 and industry_dx_rate <= 0.11021900177 and industry_all_cnt > 4796.0 and industry_dx_cnt > 448.5",
        "sample_number": 74,
        "label": 1
    },
    {
        "missclassfication_rate": 0.055555555555555552,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt <= 3.5 and industry_26 <= 0.5 and litigant_defendant_contract_dispute_cnt <= 106.0 and judge_doc_cnt > 3.5 and network_share_zhixing_cnt > 67.5",
        "sample_number": 18,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and zczjbz > 0.5 and trade_mark_cnt <= 0.5 and established_years <= 4.5 and fr_change_cnt <= 0.5 and regcap <= 95.0",
        "sample_number": 143,
        "label": 1
    },
    {
        "missclassfication_rate": 0.090909090909090912,
        "decision_path": "court_notice_is_no <= 0.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap <= 209.0 and zczjbz > 0.5 and trade_mark_cnt <= 0.5 and established_years <= 4.5 and fr_change_cnt <= 0.5 and regcap > 95.0 and cancel_cnt > 0.5",
        "sample_number": 11,
        "label": 1
    },
    {
        "missclassfication_rate": 0.066666666666666666,
        "decision_path": "court_notice_is_no <= 0.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap <= 209.0 and zczjbz > 0.5 and trade_mark_cnt <= 0.5 and established_years <= 4.5 and fr_change_cnt <= 0.5 and regcap > 95.0 and cancel_cnt <= 0.5 and industry_dx_rate > 0.0932900011539",
        "sample_number": 15,
        "label": 1
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no > 0.5 and regcap > 6.0 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt <= 3.5 and industry_26 <= 0.5 and litigant_defendant_contract_dispute_cnt <= 106.0 and judge_doc_cnt > 3.5 and network_share_zhixing_cnt <= 67.5 and regcap <= 9400.0",
        "sample_number": 200,
        "label": 0
    },
    {
        "missclassfication_rate": 0.027777777777777776,
        "decision_path": "court_notice_is_no > 0.5 and near_3_year_judgedoc_cnt <= 1.5 and utility_publish_three_year_rate <= 0.165000006557 and network_fr_share_change_cnt <= 3.5 and industry_26 <= 0.5 and litigant_defendant_contract_dispute_cnt <= 106.0 and judge_doc_cnt > 3.5 and network_share_zhixing_cnt <= 67.5 and regcap > 9400.0",
        "sample_number": 36,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no <= 0.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap <= 209.0 and zczjbz > 0.5 and trade_mark_cnt <= 0.5 and fr_change_cnt <= 0.5 and regcap > 95.0 and cancel_cnt <= 0.5 and industry_dx_rate <= 0.0932900011539 and established_years <= 3.5",
        "sample_number": 75,
        "label": 1
    },
    {
        "missclassfication_rate": 0.029411764705882353,
        "decision_path": "court_notice_is_no <= 0.5 and hy_shixin_cnt <= 5.0 and industry_dx_cnt <= 8419.5 and court_announce_litigant_cnt <= 1.5 and network_share_punish_cnt <= 2.5 and network_share_cancel_cnt <= 31.0 and regcap <= 209.0 and zczjbz > 0.5 and trade_mark_cnt <= 0.5 and established_years <= 4.5 and fr_change_cnt <= 0.5 and regcap > 95.0 and cancel_cnt <= 0.5 and industry_dx_rate <= 0.0932900011539 and established_years > 3.5",
        "sample_number": 34,
        "label": 1
    },
    {
        "missclassfication_rate": 0.020408163265306121,
        "decision_path": "court_notice_is_no > 0.5 and near_3_year_judgedoc_cnt > 1.5 and established_years <= 46.0 and regcap > 102.5 and trademark_three_year_rate <= 1.5 and industry_all_cnt <= 78776.5 and share_change_cnt > 14.5",
        "sample_number": 49,
        "label": 0
    },
    {
        "missclassfication_rate": 0.022727272727272728,
        "decision_path": "court_notice_is_no > 0.5 and near_3_year_judgedoc_cnt > 1.5 and established_years <= 46.0 and regcap > 102.5 and trademark_three_year_rate <= 1.5 and industry_all_cnt <= 78776.5 and share_change_cnt <= 14.5 and litigant_defendant_infringe_cnt > 1.5",
        "sample_number": 44,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no > 0.5 and near_3_year_judgedoc_cnt > 1.5 and established_years <= 46.0 and regcap > 102.5 and trademark_three_year_rate <= 1.5 and industry_all_cnt <= 78776.5 and share_change_cnt <= 14.5 and litigant_defendant_infringe_cnt <= 1.5 and fr_change_cnt <= 3.5",
        "sample_number": 621,
        "label": 0
    },
    {
        "missclassfication_rate": 0.058823529411764705,
        "decision_path": "court_notice_is_no > 0.5 and near_3_year_judgedoc_cnt > 1.5 and established_years <= 46.0 and regcap > 102.5 and trademark_three_year_rate <= 1.5 and industry_all_cnt <= 78776.5 and share_change_cnt <= 14.5 and litigant_defendant_infringe_cnt <= 1.5 and fr_change_cnt > 3.5 and regcap_change_cnt <= 0.5",
        "sample_number": 17,
        "label": 0
    },
    {
        "missclassfication_rate": 0.0,
        "decision_path": "court_notice_is_no > 0.5 and near_3_year_judgedoc_cnt > 1.5 and established_years <= 46.0 and regcap > 102.5 and trademark_three_year_rate <= 1.5 and industry_all_cnt <= 78776.5 and share_change_cnt <= 14.5 and litigant_defendant_infringe_cnt <= 1.5 and fr_change_cnt > 3.5 and regcap_change_cnt > 0.5",
        "sample_number": 82,
        "label": 0
    }
]

f = FeatureHelper()

class DxRiskRulesTransfer(object):
    """
    吊销风险规则转换
    """

    def predict_dx_risk_rate(self, dx_features):
        """
        :type dx_features DxFeatureDto
        :type dx_risk_re_do DxRiskReDo
        :param dx_features:
        :return: dx_risk_re_do
        """

        dx_df_dict = f.convert_to_dict(dx_features)
        for item in dx_risk_rules:
            result_list = []
            missclassfication_rate = item.get("missclassfication_rate")
            decision_path = item.get("decision_path")
            sample_number = item.get("sample_number")
            label = item.get("label")
            # "regcap_change_cnt <= 0.5 and trademark_three_year_rate <= 0.165000006557 and address_change_cnt <= 0.5 and established_years > 12.5 and judgedoc_is_no <= 0.5 and bidding_cnt > 0.5"
            if f.is_none(decision_path):
                raise Exception("内部数据异常！！！")
            result_list = self.__condition_judge(decision_path, dx_df_dict, result_list)

        return result_list

    @staticmethod
    def __condition_judge(decision_path, dx_df_dict, result_list):
        """
        规则引擎条件判断
        :param decision_path:
        :param dx_df_dict:
        :param result_list:
        :return:
        """
        decision_condition_list = str(decision_path).split("and")
        for dc in decision_condition_list:
            # ">", "<="
            # 任何一个条件不满足结束循环
            if ">" in dc:
                judge_condition_list = str(dc).split(">")
                judge_result = dx_df_dict.get(judge_condition_list[0].strip())
                if not f.is_none(judge_result):
                    if judge_result > float(judge_condition_list[1].strip()):
                        description = f.get_feature_chinese_name(judge_condition_list[0].strip())
                        result_list.append(description + " > " + str(judge_condition_list[1]).strip())
                    else:
                        result_list = []
                        return result_list
            elif "<=" in dc:
                judge_condition_list = str(dc).split("<=")
                judge_result = dx_df_dict.get(judge_condition_list[0].strip())
                if not f.is_none(judge_result):
                    if judge_result <= float(judge_condition_list[1].strip()):
                        description = f.get_feature_chinese_name(judge_condition_list[0].strip())
                        result_list.append(description + " <= " + str(judge_condition_list[1].strip()))
                    else:
                        result_list = []
                        return result_list
        return result_list



if __name__ == '__main__':
    '''
    将规则引擎转换为
    :return:
    '''
    dx_risk_rules_list = []
    for item in dx_risk_rules:
        missclassfication_rate = item.get("missclassfication_rate")
        decision_path = item.get("decision_path")
        sample_number = item.get("sample_number")
        label = item.get("label")
        decision_condition_list = str(decision_path).split("and")
        description_list = []
        for dc in decision_condition_list:
            # ">", "<="
            # 任何一个条件不满足结束循环
            try:
                if ">" in dc:
                    judge_condition_list = str(dc).split(">")
                    description = f.get_feature_chinese_name(judge_condition_list[0].strip())
                    # description = description.decode('unicode_escape')
                    description_list.append(description + " > " + str(judge_condition_list[1]))
                elif "<=" in dc:
                    judge_condition_list = str(dc).split("<=")
                    description = f.get_feature_chinese_name(judge_condition_list[0].strip())
                    # description = description.decode('unicode_escape')
                    description_list.append(description +" <= " + str(judge_condition_list[1]))
            except Exception as e:
                traceback.print_exc()
        description_list =" and ".join(description_list)
        dx_risk_rules_list.append({
                    "missclassfication_rate": missclassfication_rate,
                    "decision_path": description_list,
                    "sample_number": sample_number,
                    "label": label
            })

    f.write_json("/home/sinly/ljtstudy/code/risk_rules/sklearn_result01/bankrupt_risk_rule_chinese.json", dx_risk_rules_list)



# if __name__ == '__main__':
#     import pandas as pd
#     import json
#     feature_name = ["_c0", "_c1", "established_years", "regcap_change_cnt", "trademark_three_year_rate",
#                     "address_change_cnt",
#                     "regcap", "network_share_cancel_cnt", "cancel_cnt", "judgedoc_is_no", "industry_dx_rate",
#                     "judgedoc_cnt", "bidding_three_year_rate", "bidding_cnt", "fr_change_cnt", "industry_dx_cnt",
#                     "share_change_cnt", "industry_all_cnt", "network_fr_share_change_cnt", "zczjbz",
#                     "network_share_zhixing_cnt", "invent_publish_three_year_rate", "invent_publish_cnt",
#                     "court_announce_cnt", "judge_doc_cnt", "litigant_defendant_infringe_cnt", "near_1_year_shixin_cnt"]
#     file_path = "/home/sinly/ljtstudy/back/new_version_all_features.csv"
#     df = pd.read_csv(file_path)
#     # 正常
#     # df_p = df[df['_c1'] == 1].head(1000)
#     df = df[df['_c1'] == 1].head(500)
#     # # 吊销
#     # df_n = df[df['_c1'] == 2].head(100)
#     # frames = [df_p, df_n]
#     # df = pd.concat(frames)
#     df = df.fillna(0)
#     company_list = df["_c0"].tolist()
#     df = df[feature_name]
#     df1 = df[feature_name[1:]].apply(lambda x: f.string_list_to_float(x))
#     df[feature_name[1:]] = df1
#     df['zczjbz'] = df.zczjbz.apply(lambda x: f.is_rmb(x))
#     df = df.fillna(0)
#     for company in company_list:
#         feature = df[df["_c0"] == company][feature_name]
#         dx_risk_rt = DxRiskRulesTransfer()
#         dx_features = DxFeatureDto()
#         primary_label = feature["_c1"].values[0]
#         dx_features.zczjbz = feature["zczjbz"].values[0]
#         dx_features.company_name = feature["_c0"].values[0]
#         dx_features.share_change_cnt = feature["share_change_cnt"].values[0]
#         dx_features.judgedoc_cnt = feature["judgedoc_cnt"].values[0]
#         dx_features.address_change_cnt = feature["address_change_cnt"].values[0]
#         dx_features.bidding_cnt = feature["bidding_cnt"].values[0]
#         dx_features.bidding_three_year_rate = feature["bidding_three_year_rate"].values[0]
#         dx_features.cancel_cnt = feature["cancel_cnt"].values[0]
#         dx_features.court_announce_cnt = feature["court_announce_cnt"].values[0]
#         dx_features.established_years = feature["established_years"].values[0]
#         dx_features.fr_change_cnt = feature["fr_change_cnt"].values[0]
#         dx_features.industry_all_cnt = feature["industry_all_cnt"].values[0]
#         dx_features.industry_dx_cnt = feature["industry_dx_cnt"].values[0]
#         dx_features.industry_dx_rate = feature["industry_dx_rate"].values[0]
#         dx_features.invent_publish_cnt = feature["zczjbz"].values[0]
#         dx_features.invent_publish_three_year_rate = feature["invent_publish_three_year_rate"].values[0]
#         dx_features.judge_doc_cnt = feature["judge_doc_cnt"].values[0]
#         dx_features.judgedoc_is_no = feature["judgedoc_is_no"].values[0]
#         dx_features.litigant_defendant_infringe_cnt = feature["litigant_defendant_infringe_cnt"].values[0]
#         dx_features.near_1_year_shixin_cnt = feature["near_1_year_shixin_cnt"].values[0]
#         dx_features.network_fr_share_change_cnt = feature["network_fr_share_change_cnt"].values[0]
#         dx_features.network_share_cancel_cnt = feature["network_share_cancel_cnt"].values[0]
#         dx_features.network_share_zhixing_cnt = feature["network_share_zhixing_cnt"].values[0]
#         dx_features.regcap = feature["regcap"].values[0]
#         dx_features.regcap_change_cnt = feature["regcap_change_cnt"].values[0]
#         dx_features.trademark_three_year_rate = feature["trademark_three_year_rate"].values[0]
#
#         dx_risk_re_do = dx_risk_rt.predict_dx_risk_rate(dx_features=dx_features)
#         clf = f.load_model("dx_tree.model")
#         mode_predict_proba = clf.predict_proba(feature[feature_name[2:]].as_matrix())[0]
#         mode_predict = clf.predict(feature[feature_name[2:]].as_matrix())[0]
#         print("mode_predict_proba="+str(mode_predict_proba))
#         print("mode_predict="+str(mode_predict))
#         print(company + " primary_label= " + str(primary_label) + " <=> predict_label= "+ str(dx_risk_re_do.label) + " : "+ str(json.dumps(dx_risk_re_do, ensure_ascii=False, default=lambda x: x.__dict__)))
