#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 
@site: 
@software: PyCharm
@file: feature_helper.py
@time: 18-6-1 下午5:53
"""



class FeatureHelper(object):
    """
    特征帮助类
    """
    code = {'network_share_shixin_cnt': u'网络图股东或者对外投资企业的失信次数',
            'network_share_zhixing_cnt': u'网络图股东或者对外投资企业的执行次数',
            'network_share_sszc_cnt': u'网络图股东或者对外投资企业司法拍卖',
            'network_share_punish_cnt': u'网络图股东或者对外投资企业行政处罚',
            'network_share_judge_doc_cnt': u'网络图股东或者对外投资企业作为被告的裁判文书次数',
            'network_share_cancel_cnt': u'网络图股东或者对外投资企业有吊销企业的数量',
            'judgedoc_is_no': u'裁判文书与否',
            'judgedoc_cnt': u'裁判文书次数',
            'litigant_defendant_cnt': u'裁判文书被告次数',
            'near_3_year_judgedoc_cnt': u'近3年裁判文书次数',
            'near_2_year_judgedoc_cnt': u'近2年裁判文书次数',
            'near_1_year_judgedoc_cnt': u'近1年裁判文书次数',
            'litigant_defendant_contract_dispute_cnt': u'裁判文书被告合同纠纷次数',
            'litigant_defendant_bust_cnt': u'裁判文书被告与破产有关纠纷次数',
            'litigant_defendant_infringe_cnt': u'裁判文书被告侵权责任纠纷次数',
            'litigant_defendant_Intellectual_property_owner_cnt': u'裁判文书被告知识产权权属、侵权纠纷次数',
            'litigant_defendant_unjust_enrich_cnt': u'裁判文书被告不当得利纠纷次数',
            'litigant_result_sum_money': u'裁判文书被告案件判决总金额',
            'net_judgedoc_defendant_cnt': u'关联公司裁判文书被告次数',
            'the_last_shi_xin_label': u'失信与否',
            'shixin_cnt': u'失信次数',
            'shixin_is_no': u'是否失信',
            'near_3_year_shixin_cnt': u'近3年内失信次数',
            'near_2_year_shixin_cnt': u'近2年内失信次数',
            'near_1_year_shixin_cnt': u'近1年内失信次数',
            'court_announce_is_no': u'开庭公告与否',
            'court_announce_cnt': u'开庭公告次数',
            'court_announce_litigant_cnt': u'开庭公告被告次数',
            'court_notice_is_no': u'法院公告与否',
            'court_notice_cnt': u'法院公告次数',
            'court_notice_litigant_cnt': u'法院公告被告次数',
            'industry_13': u'棉、麻、糖、烟草种植',
            'industry_26': u'化学原料和化学制品制造业',
            'industry_519': u'其他批发业',
            'industry_18': u'纺织服装、服饰业',
            'industry_1810': u'机织服装制造',
            'industry_62': u'褐煤开采洗选',
            'industry': u'行业',
            'industry_dx_rate': u'行业企业吊销率',
            'industry_dx_cnt': u'行业企业吊销数量',
            'industry_all_cnt': u'行业企业数量',
            'province': u'省份',
            'regcap': u'注册资本（量级万）',
            'zczjbz': u'注册资本币种',
            'established_years': u'成立年限',
            'fr_change_cnt': u'法人变更次数',
            'address_change_cnt': u'地址变更次数',
            'regcap_change_cnt': u'注册资本变更次数',
            'share_change_cnt': u'股东变更次数',
            'network_fr_share_change_cnt': u'网络图法人对外投资或者任职的公司股权变更次数',
            'hy_shixin_cnt': u'网络图法人对外投资或者任职的公司失信次数',
            'zhixing_cnt': u'网络图法人对外投资或者任职的公司执行次数',
            'sszc_cnt': u'网络图法人对外投资或者任职的公司司法拍卖',
            'punish_cnt': u'网络图法人对外投资或者任职的公司行政处罚',
            'judge_doc_cnt': u'网络图法人对外投资或者任职的公司作为被告的裁判文书次数',
            'cancel_cnt': u'网络图法人对外投资或者任职的公司有吊销企业的数量',
            'bidding_cnt': u'(3年内)招投标次数',
            'bidding_three_year_rate': u'(3年内)平均每年招投标次数',
            'is_black_list': u'是否黑名单',
            'is_escape': u'是否跑路',
            'is_diff_raise_money': u'是否提现困难',
            'is_stop_busi': u'是否停止营业',
            'is_lost_with_money': u'是否失联跑路',
            'is_just_lost': u'是否平台失联',
            'invent_publish_cnt': u'(3年内)发明公布数量',
            'invent_patent_cnt': u'(3年内)发明专利数量',
            'utility_publish_cnt': u'(3年内)实用新型数量',
            'invent_publish_three_year_rate': u'(3年内)平均每年拥有的发明公布数量',
            'invent_patent_three_year_rate': u'(3年内)平均每年拥有的发明专利数量',
            'utility_publish_three_year_rate': u'（3年内）平均每年拥有的实用新型数量',
            'warn_cnt': u'（3年内）警告次数',
            'fine_cnt': u'（3年内）罚款次数',
            'revoking_cnt': u'（3年内）吊销营业执照次数',
            'warn_cnt_three_year_rate': u'（3年内）平均警告次数',
            'fine_cnt_three_year_rate': u'（3年内）平均罚款次数',
            'revoking_cnt_three_year_rate': u'（3年内）平均吊销营业执照次数',
            'estate_auction_cnt': u'（3年内）动产拍卖次数',
            'real_estate_auction_cnt': u'（3年内）不动产拍卖次数',
            'trade_mark_cnt': u'商标注册数量',
            'trademark_three_year_rate': u'（3年内）平均每年注册的商标数量',
            'network_share_or_pos_shixin_cnt': u'网络图股东或者对外投资企业的失信次数'
            }

    @staticmethod
    def is_none(d):
        return (d is None or d == 'None' or
                d == '?' or
                d == '' or
                d == 'NULL' or
                d == 'null')

    @staticmethod
    def write_json(path, data):
        '''
         保存清洗数据
        '''
        import json
        import traceback
        print(json.dumps(data,ensure_ascii=False,indent=4,default=lambda x:str(x)))
        try:
            with open(path, "w") as outfile:
                json.dump(data, outfile, indent=4)
        except Exception as e:
            traceback.print_exc()

    @staticmethod
    def convert_to_dict(obj):
        '''把Object对象转换成Dict对象'''
        dict = {}
        dict.update(obj.__dict__)
        return dict

    @staticmethod
    def load_model(model_name):
        from sklearn.externals import joblib
        return joblib.load(model_name)

    @staticmethod
    def string_list_to_float(list01):
        res = []
        for item in list01:
            try:
                res.append(float(item))
            except:
                # print(item)
                res.append(0.0)
        return res

    @staticmethod
    def is_rmb(x):
        if x == 156 or x == 0:
            return 1
        else:
            return 0

    def get_feature_chinese_name(self, feature_name):
        if not self.is_none(feature_name):
            feature_chinese_name = self.code.get(feature_name)
            return feature_chinese_name
        else:
            raise Exception("参数异常！！！")


if __name__ == '__main__':
    f = FeatureHelper()
    print(f.get_feature_chinese_name("network_share_or_pos_shixin_cnt"))
