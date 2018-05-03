# -*- coding:utf-8 -*-
'''
 特征统计:
  scp ./ljt_feature_extract.py       scdata@192.168.31.10:/home/scdata/app/python/risk-model/feature_extract_ljt/
spark-submit --master spark://192.168.31.10:7077 --executor-memory 20G --total-executor-cores 15 /home/scdata/app/python/risk-model/etl_ljt_script/feature_extract_ljt/ljt_feature_extract.py
Created on 2018年01月29日
'''

from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from pyspark.sql import SparkSession, SQLContext
from pyspark.sql import Row
import time
import datetime
import os
import json
hdfspath = 'hdfs://192.168.31.10:9000'
# hdfspath = 'hdfs://192.168.31.242:9000'
Etlreadpath = hdfspath + "/scdata/riskModel/riskModelDataETL/"
# Etlreadpath = hdfspath + "/scdata/riskModel/riskModelData/"
savepath =hdfspath +"/scdata/riskModel/features/"
feature_path = hdfspath+"/scdata/riskModel/"
hdfssourcefile = hdfspath + "/scdata/riskModel/riskModelData/"
hdfsSaveStats = hdfspath +'/scdata/riskModel/stats/'
myfeature_path =hdfspath +'/scdata/riskModel/features/featuredata/'
sparkpath = "spark://192.168.31.10:7077"
# sparkpath = "spark://192.168.31.242:7077"


# Type converter
def isNone(d):
    return (d is None or d == 'None' or
            d == '?' or
            d == '' or
            d == 'NULL' or
            d == 'null')


def empty_deal(data):
    '''
    空表示没有,非空表示有
    :param data:
    :return:
    '''
    if isNone(data):
        data = 0
    else:
        data = 1
    return data

def empty_deal_cnt(data):
    '''
    空表示没有,非空表示有
    :param data:
    :return:
    '''
    if isNone(data):
        data = 0
    else:
        try:
            data = int(data)
        except Exception as e:
            data = 0
    return data

def cmp_years(date):
    year = 0
    if isNone(date):
        year = 0
    else:
        try:
            year = datetime.datetime.now().year - float(str(date)[:4])
        except Exception as e:
            year = 0
    return year

def feature_extract_shixin(spark, sc):
    '''
    吊销风险预测模型-特征提取
    :return:
    '''
    sqlContext = SQLContext(sparkContext=sc)
    sqlContext.registerFunction("empty_deal", lambda x: empty_deal(x))
    sqlContext.registerFunction("empty_deal_cnt", lambda x: empty_deal_cnt(x))
    sqlContext.registerFunction("cmp_years", lambda x: cmp_years(x))
    dfshixin = sqlContext.read.csv(Etlreadpath + 'court_shixin_company_new.csv',
                             header=True)
    # dfshixin.show()
    dfshixin.createOrReplaceTempView('shixin_cmp')
    # sqlContext.sql("select   count(1)  from shixin_cmp ").show()
    dfshixincnt = sqlContext.sql("select company_name, count(1) as shixin_cnt from shixin_cmp GROUP BY company_name")
    dfshixincnt.createOrReplaceTempView('shixin_cnt')
    dfshixin3yearcnt = sqlContext.sql("select company_name, count(1) as near_3_year_shixin_cnt from shixin_cmp WHERE  cmp_years(publish_date)>=3 "
                                      " GROUP BY company_name")
    # dfshixin3yearcnt.show()
    dfshixin3yearcnt.createOrReplaceTempView('shixin_cmp_3year_cnt')
    dfshixin2yearcnt = sqlContext.sql(
        "select company_name, count(1) as near_2_year_shixin_cnt from shixin_cmp WHERE  cmp_years(publish_date)>=2 "
        " GROUP BY company_name")
    dfshixin2yearcnt.createOrReplaceTempView('shixin_cmp_2year_cnt')
    dfshixin1yearcnt = sqlContext.sql(
        "select company_name, count(1) as near_1_year_shixin_cnt from shixin_cmp WHERE  cmp_years(publish_date)>=1 "
        " GROUP BY company_name")
    dfshixin1yearcnt.createOrReplaceTempView('shixin_cmp_1year_cnt')
    nearyear = sqlContext.sql(
        "select sx3.company_name,  empty_deal_cnt(sx3.near_3_year_shixin_cnt) as near_3_year_shixin_cnt, "
        " empty_deal_cnt(sx2.near_2_year_shixin_cnt) as near_2_year_shixin_cnt,"
        " empty_deal_cnt(sx1.near_1_year_shixin_cnt) as near_1_year_shixin_cnt "
        " from  shixin_cmp_3year_cnt sx3, shixin_cmp_2year_cnt sx2,shixin_cmp_1year_cnt sx1 "
        " WHERE sx2.company_name=sx3.company_name   AND sx3.company_name=sx1.company_name")
    nearyear.createOrReplaceTempView('nearyear')
    dfshixinfeature = sqlContext.sql(
        "select sxc.company_name,sxc.shixin_cnt,empty_deal_cnt(ny.near_3_year_shixin_cnt) as near_3_year_shixin_cnt, "
        " empty_deal_cnt(ny.near_2_year_shixin_cnt) as near_2_year_shixin_cnt,"
        " empty_deal_cnt(ny.near_1_year_shixin_cnt) as near_1_year_shixin_cnt "
        " from  shixin_cnt sxc LEFT JOIN nearyear ny ON sxc.company_name=ny.company_name")
    dfshixinfeature.createOrReplaceTempView('dfshixinfeature01')

    base_info = sqlContext.read.csv(Etlreadpath + 'base_info_name.csv',
                                    header=True)
    # base_info.show()
    base_info.createOrReplaceTempView('baseinfo_cmp')
    # 去重
    base_info01 = sqlContext.sql("select  bs.name as company_name, count(bs.name) as cnt from baseinfo_cmp  bs GROUP BY bs.name")
    base_info01.createOrReplaceTempView('baseinfo01_cmp')
    resdf = sqlContext.sql("select  bs.company_name,empty_deal(sx.company_name) AS shixin_is_no,"
                           "empty_deal_cnt(sx.shixin_cnt) as shixin_cnt, empty_deal_cnt(sx.near_3_year_shixin_cnt) as near_3_year_shixin_cnt,"
                           "empty_deal_cnt(sx.near_2_year_shixin_cnt) as near_2_year_shixin_cnt,"
                           "empty_deal_cnt(sx.near_1_year_shixin_cnt) as near_1_year_shixin_cnt from baseinfo01_cmp as bs LEFT JOIN dfshixinfeature01 AS sx "
                           " ON bs.company_name=sx.company_name where length(bs.company_name) >= 5 ")
    resdf.createOrReplaceTempView('shixin_feature')
    sqlContext.sql("select * from shixin_feature sf WHERE sf.shixin_cnt > 0").show()
    sqlContext.sql("select COUNT (*) from shixin_feature sf WHERE sf.shixin_cnt > 0").show()

    resdf.repartition(1).write.csv(os.path.join(savepath, "shixin_feature.csv"), mode='overwrite', header=True)

def contains_String(s0,s):
    state = 0
    if isNone(s):
        state = 0
    elif s0 in s:
        state = 1
    else:
        state = 0
    return state

def judgedoc_money(d):
    '''
    3"win",2"lost",1"part",0"unknown"
    :param d:
    :return:
    '''
    if isNone(d):
        d = 0
    else:
        try:
            d = float(d)
        except :
            d = 0
    return d



def feature_extract_judgedoc(spark, sc):
    '''
    吊销风险预测模型-特征提取
    :return:
    '''
    sqlContext = SQLContext(sparkContext=sc)
    sqlContext.registerFunction("empty_deal", lambda x: empty_deal(x))
    sqlContext.registerFunction("empty_deal_cnt", lambda x: empty_deal_cnt(x))
    sqlContext.registerFunction("cmp_years", lambda x: cmp_years(x))
    sqlContext.registerFunction("judgedoc_money", lambda x: judgedoc_money(x))
    sqlContext.registerFunction("contains_String", lambda s0, s: contains_String(s0, s))
    judgedoc = sqlContext.read.csv(Etlreadpath + 'judgedoc_litigant.csv',
                                   header=True)
    judgedoc.createOrReplaceTempView('judgedoc_cmp')
    litigant_result_sum_money = sqlContext.sql("select  litigant_name as company_name,"
                                  " sum(judgedoc_money(case_result_money)) as litigant_result_sum_money "
                                  "from judgedoc_cmp GROUP BY litigant_name")
    litigant_result_sum_money.createOrReplaceTempView('judgedoc_sum_money')
    # sqlContext.sql("select * from judgedoc_sum_money WHERE litigant_result_sum_money!=0").show()

    litigant_defendant_cnt = sqlContext.sql(
        "select  litigant_name AS company_name, count(1) as litigant_defendant_cnt from judgedoc_cmp"
        " WHERE contains_String('被告',case_type)>0 GROUP BY litigant_name")
    litigant_defendant_cnt.createOrReplaceTempView('litigant_defendant_cnt')
    dfjudgedoccnt = sqlContext.sql(
        "select  litigant_name AS company_name, count(1) as judgedoc_cnt from judgedoc_cmp GROUP BY litigant_name")
    dfjudgedoccnt.createOrReplaceTempView('judgedoc_cnt')

    dfjudgedoccnt = sqlContext.sql(
        "select  cn.*,empty_deal(df.litigant_defendant_cnt) AS  litigant_defendant_cnt from judgedoc_cnt cn LEFT JOIN "
        " litigant_defendant_cnt df ON cn.company_name=df.company_name")
    dfjudgedoccnt.createOrReplaceTempView('judgedoc_cnt')

    dfjudgedoc3yearcnt = sqlContext.sql(
        "select litigant_name as company_name, count(1) as near_3_year_judgedoc_cnt from judgedoc_cmp WHERE  cmp_years(publish_date)>=3 "
        " GROUP BY litigant_name")
    # dfjudgedoc3yearcnt.show()
    dfjudgedoc3yearcnt.createOrReplaceTempView('judgedoc_cmp_3year_cnt')
    dfjudgedoc2yearcnt = sqlContext.sql(
        "select litigant_name as company_name, count(1) as near_2_year_judgedoc_cnt from judgedoc_cmp WHERE  cmp_years(publish_date)>=2 "
        " GROUP BY litigant_name")
    dfjudgedoc2yearcnt.createOrReplaceTempView('judgedoc_cmp_2year_cnt')
    dfjudgedoc1yearcnt = sqlContext.sql(
        "select litigant_name as company_name, count(1) as near_1_year_judgedoc_cnt from judgedoc_cmp WHERE  cmp_years(publish_date)>=1 "
        " GROUP BY litigant_name")
    dfjudgedoc1yearcnt.createOrReplaceTempView('judgedoc_cmp_1year_cnt')
    nearyear = sqlContext.sql(
        "select sx3.company_name,  empty_deal_cnt(sx3.near_3_year_judgedoc_cnt) as near_3_year_judgedoc_cnt, "
        " empty_deal_cnt(sx2.near_2_year_judgedoc_cnt) as near_2_year_judgedoc_cnt,"
        " empty_deal_cnt(sx1.near_1_year_judgedoc_cnt) as near_1_year_judgedoc_cnt "
        " from  judgedoc_cmp_3year_cnt sx3, judgedoc_cmp_2year_cnt sx2,judgedoc_cmp_1year_cnt sx1 "
        " WHERE sx2.company_name=sx3.company_name   AND sx3.company_name=sx1.company_name")
    nearyear.createOrReplaceTempView('nearyear')
    dfjudgedocfeature = sqlContext.sql(
        "select sxc.company_name,sxc.judgedoc_cnt,"
        " sxc.litigant_defendant_cnt, empty_deal_cnt(ny.near_3_year_judgedoc_cnt) as near_3_year_judgedoc_cnt, "
        " empty_deal_cnt(ny.near_2_year_judgedoc_cnt) as near_2_year_judgedoc_cnt,"
        " empty_deal_cnt(ny.near_1_year_judgedoc_cnt) as near_1_year_judgedoc_cnt "
        " from  judgedoc_cnt sxc LEFT JOIN nearyear ny ON sxc.company_name=ny.company_name")
    dfjudgedocfeature.createOrReplaceTempView('dfjudgedocfeature01')
    contract_dispute = sqlContext.sql(
        "select litigant_name as company_name, count(1) as litigant_defendant_contract_dispute_cnt from judgedoc_cmp"
        " WHERE  contains_String('合同纠纷',case_reason)>=1 "
        " GROUP BY litigant_name")
    # contract_dispute.show()
    contract_dispute.createOrReplaceTempView('contract_dispute')
    contract_dispute = sqlContext.sql("select sxc.company_name,sxc.judgedoc_cnt,"
                                      " empty_deal_cnt(cd.litigant_defendant_contract_dispute_cnt) as litigant_defendant_contract_dispute_cnt "
                                      " from judgedoc_cnt sxc LEFT JOIN contract_dispute cd ON sxc.company_name=cd.company_name")
    contract_dispute.createOrReplaceTempView('contract_dispute')
    bust = sqlContext.sql(
        "select litigant_name as company_name, count(1) as litigant_defendant_bust_cnt from judgedoc_cmp"
        "  WHERE  contains_String('与破产有关的纠纷',case_reason)>=1 "
        " GROUP BY litigant_name")
    bust.createOrReplaceTempView('bust')
    bust = sqlContext.sql(
        "select sxc.company_name,sxc.judgedoc_cnt,"
        " empty_deal_cnt(cd.litigant_defendant_bust_cnt) as litigant_defendant_bust_cnt "
        " from judgedoc_cnt sxc LEFT JOIN bust cd ON sxc.company_name=cd.company_name")
    bust.createOrReplaceTempView('bust')

    infringe = sqlContext.sql(
        "select litigant_name as company_name, count(1) as litigant_defendant_infringe_cnt from judgedoc_cmp"
        "  WHERE  contains_String('侵权责任纠纷',case_reason)>=1 "
        " GROUP BY litigant_name")
    infringe.createOrReplaceTempView('infringe')
    infringe = sqlContext.sql(
        "select sxc.company_name,sxc.judgedoc_cnt,empty_deal_cnt(cd.litigant_defendant_infringe_cnt) as litigant_defendant_infringe_cnt "
        " from judgedoc_cnt sxc LEFT JOIN infringe cd ON sxc.company_name=cd.company_name")
    infringe.createOrReplaceTempView('infringe')

    property_owner = sqlContext.sql(
        "select litigant_name as company_name, count(1) as litigant_defendant_Intellectual_property_owner_cnt from judgedoc_cmp"
        "  WHERE  contains_String('知识产权权属、侵权纠纷',case_reason)>=1 "
        " GROUP BY litigant_name")
    property_owner.createOrReplaceTempView('property_owner')
    property_owner = sqlContext.sql(
        "select sxc.company_name,sxc.judgedoc_cnt,empty_deal_cnt(cd.litigant_defendant_Intellectual_property_owner_cnt) as litigant_defendant_Intellectual_property_owner_cnt "
        " from judgedoc_cnt sxc LEFT JOIN property_owner cd ON sxc.company_name=cd.company_name")
    property_owner.createOrReplaceTempView('property_owner')

    unjust_enrich = sqlContext.sql(
        "select litigant_name as company_name, count(1) as litigant_defendant_unjust_enrich_cnt from judgedoc_cmp"
        "  WHERE  contains_String('不当得利纠纷',case_reason)>=1 "
        " GROUP BY litigant_name")
    unjust_enrich.createOrReplaceTempView('unjust_enrich')
    unjust_enrich = sqlContext.sql(
        "select sxc.company_name,sxc.judgedoc_cnt, empty_deal_cnt(cd.litigant_defendant_unjust_enrich_cnt) as litigant_defendant_unjust_enrich_cnt "
        " from judgedoc_cnt sxc LEFT JOIN unjust_enrich cd ON sxc.company_name=cd.company_name")
    unjust_enrich.createOrReplaceTempView('unjust_enrich')

    dfjudgedocfeature02 = sqlContext.sql(
        "select cd.company_name, cd.judgedoc_cnt, litigant_defendant_contract_dispute_cnt, "
        "litigant_defendant_infringe_cnt, "
        " litigant_defendant_Intellectual_property_owner_cnt, "
        "litigant_defendant_bust_cnt, litigant_defendant_unjust_enrich_cnt"
        " from contract_dispute cd,bust b,infringe fr,property_owner po,unjust_enrich ue"
        " WHERE cd.company_name=b.company_name AND cd.company_name=fr.company_name "
        " AND cd.company_name=po.company_name AND cd.company_name=ue.company_name ")
    dfjudgedocfeature02.createOrReplaceTempView('dfjudgedocfeature02')

    dfjudgedocfeature03 = sqlContext.sql(
        "select f01.company_name, f01.judgedoc_cnt, "
        " f01.litigant_defendant_cnt, empty_deal_cnt(f01.near_3_year_judgedoc_cnt) as near_3_year_judgedoc_cnt, "
        " empty_deal_cnt(f01.near_2_year_judgedoc_cnt) as near_2_year_judgedoc_cnt,"
        " empty_deal_cnt(f01.near_1_year_judgedoc_cnt) as near_1_year_judgedoc_cnt, "
        " f02.litigant_defendant_contract_dispute_cnt, "
        " f02.litigant_defendant_infringe_cnt, "
        " f02.litigant_defendant_Intellectual_property_owner_cnt, "
        " f02.litigant_defendant_bust_cnt, litigant_defendant_unjust_enrich_cnt"
        " from  dfjudgedocfeature01 f01,dfjudgedocfeature02 f02 "
        " WHERE   f02.company_name=f01.company_name")
    dfjudgedocfeature03.createOrReplaceTempView('dfjudgedocfeature03')

    dfjudgedocfeature04 = sqlContext.sql(
        "select f03.*,   jc.litigant_result_sum_money "
        " from  judgedoc_sum_money jc,dfjudgedocfeature03 f03"
        " WHERE   jc.company_name=f03.company_name ")
    dfjudgedocfeature04.createOrReplaceTempView('dfjudgedocfeature04')
    # dfjudgedocfeature04.show()

    base_info = sqlContext.read.csv(Etlreadpath + 'base_info_name.csv',
                                    header=True)
    # base_info.show()
    base_info.createOrReplaceTempView('baseinfo_cmp')
    # 去重
    base_info01 = sqlContext.sql(
        "select  bs.name as company_name, count(bs.name) as cnt from baseinfo_cmp  bs GROUP BY bs.name")
    base_info01.createOrReplaceTempView('baseinfo01_cmp')
    resdf = sqlContext.sql("select  bs.company_name,empty_deal(sx.company_name) AS judgedoc_is_no,"
                           "empty_deal_cnt(sx.judgedoc_cnt) as judgedoc_cnt, "
                           "empty_deal_cnt(sx.litigant_defendant_cnt) as litigant_defendant_cnt, "
                           "empty_deal_cnt(sx.near_3_year_judgedoc_cnt) as near_3_year_judgedoc_cnt,"
                           "empty_deal_cnt(sx.near_2_year_judgedoc_cnt) as near_2_year_judgedoc_cnt,"
                           "empty_deal_cnt(sx.near_1_year_judgedoc_cnt) as near_1_year_judgedoc_cnt, "
                           "empty_deal_cnt(sx.litigant_defendant_contract_dispute_cnt) as litigant_defendant_contract_dispute_cnt, "
                           "empty_deal_cnt(sx.litigant_defendant_bust_cnt) as litigant_defendant_bust_cnt, "
                           "empty_deal_cnt(sx.litigant_defendant_infringe_cnt) as litigant_defendant_infringe_cnt, "
                           "empty_deal_cnt(sx.litigant_defendant_Intellectual_property_owner_cnt) as litigant_defendant_Intellectual_property_owner_cnt, "
                           "empty_deal_cnt(sx.litigant_defendant_unjust_enrich_cnt) as litigant_defendant_unjust_enrich_cnt, "
                           "empty_deal_cnt(sx.litigant_result_sum_money) as litigant_result_sum_money "
                           "from baseinfo01_cmp as bs LEFT JOIN dfjudgedocfeature04 AS sx "
                           " ON bs.company_name=sx.company_name where length(bs.company_name) >= 5 ")
    resdf.createOrReplaceTempView('judgedoc_feature')
    resdf.repartition(1).write.csv(os.path.join(savepath, "judgedoc_feature.csv"), mode='overwrite', header=True)
    sqlContext.sql("select * from judgedoc_feature sf WHERE sf.litigant_result_sum_money != 0").show()


def feature_extract_court(spark, sc):
    '''
        吊销风险预测模型-特征提取
        :return:
    '''
    sqlContext = SQLContext(sparkContext=sc)
    sqlContext.registerFunction("empty_deal", lambda x: empty_deal(x))
    sqlContext.registerFunction("empty_deal_cnt", lambda x: empty_deal_cnt(x))
    sqlContext.registerFunction("cmp_years", lambda x: cmp_years(x))
    sqlContext.registerFunction("judgedoc_result", lambda x: judgedoc_money(x))
    sqlContext.registerFunction("contains_String", lambda s0, s: contains_String(s0, s))
    # 法院公告
    df01 = sqlContext.read.csv(Etlreadpath + 'sc_courtannouncement_litigant.csv',
                                   header=True)
    df01.createOrReplaceTempView('court_announcement_cmp')
    # 开庭公告
    df02 = sqlContext.read.csv(Etlreadpath + 'sc_courtnotice_litigant.csv',
                                   header=True)
    df02.createOrReplaceTempView('court_notice_cmp')
    df02.show()
    # sqlContext.sql("select   count(1)  from shixin_cmp ").show()
    # 开庭公告被告次数
    court_announce_litigant_cnt = sqlContext.sql(
        "select  litigant_name AS company_name, count(1) as court_announce_litigant_cnt from court_announcement_cmp"
        " WHERE contains_String('被告',litigant_type)>0 GROUP BY litigant_name")
    court_announce_litigant_cnt.createOrReplaceTempView('court_announce_litigant_cnt')
    # court_announce_litigant_cnt.show()
    # 法院公告被告次数
    court_notice_litigant_cnt = sqlContext.sql(
        "select  litigant_name AS company_name, count(1) as court_notice_litigant_cnt from court_notice_cmp"
        " WHERE contains_String('被告',litigant_type)>0 GROUP BY litigant_name")
    court_notice_litigant_cnt.createOrReplaceTempView('court_notice_litigant_cnt')
    # court_notice_litigant_cnt.show()
    # 开庭公告次数
    court_announce_cnt = sqlContext.sql("select litigant_name AS company_name, count(1) as court_announce_cnt from court_announcement_cmp GROUP BY litigant_name")
    court_announce_cnt.createOrReplaceTempView('court_announce_cnt')

    # 法院公告次数
    court_notice_cnt = sqlContext.sql("select litigant_name AS company_name, count(1) as court_notice_cnt from court_notice_cmp GROUP BY litigant_name")
    court_notice_cnt.createOrReplaceTempView('court_notice_cnt')

    #开庭公告特征合并
    dfannouncefeature01 = sqlContext.sql("select ca.*,empty_deal_cnt(cal.court_announce_litigant_cnt) as court_announce_litigant_cnt "
                                         " from court_announce_cnt ca LEFT JOIN court_announce_litigant_cnt cal "
                                         " ON ca.company_name =  cal.company_name")
    dfannouncefeature01.createOrReplaceTempView('dfannouncefeature01')
    # dfannouncefeature01.show()

    #法院公告特征合并
    dfnoticefeature01 = sqlContext.sql("select ca.*,empty_deal_cnt(cal.court_notice_litigant_cnt) as court_notice_litigant_cnt "
                                         " from court_notice_cnt ca LEFT JOIN court_notice_litigant_cnt cal "
                                         " ON ca.company_name =  cal.company_name")
    dfnoticefeature01.createOrReplaceTempView('dfnoticefeature01')
    # dfnoticefeature01.show()

    base_info = sqlContext.read.csv(Etlreadpath + 'base_info_name.csv',
                                    header=True)
    # base_info.show()
    base_info.createOrReplaceTempView('baseinfo_cmp')
    # 去重
    base_info01 = sqlContext.sql(
        "select  bs.name as company_name, count(bs.name) as cnt from baseinfo_cmp  bs GROUP BY bs.name")
    base_info01.createOrReplaceTempView('baseinfo01_cmp')
    # 与基表合并抽出开庭公告特征
    court_announce_feature = sqlContext.sql("select  bs.company_name,empty_deal(sx.company_name) AS court_announce_is_no,"
                           "  empty_deal_cnt(sx.court_announce_cnt) as court_announce_cnt, "
                           "  empty_deal_cnt(sx.court_announce_litigant_cnt) as court_announce_litigant_cnt"
                           " from baseinfo01_cmp as bs LEFT JOIN dfannouncefeature01 AS sx "
                           " ON bs.company_name=sx.company_name where length(bs.company_name) >= 5 ")
    court_announce_feature.createOrReplaceTempView('court_announce_feature')

    # 与基表合并抽出法院公告特征
    court_notice_feature = sqlContext.sql("select bs.company_name,empty_deal(sx.company_name) AS court_notice_is_no,"
                           "  empty_deal_cnt(sx.court_notice_cnt) as court_notice_cnt, "
                           "  empty_deal_cnt(sx.court_notice_litigant_cnt) as court_notice_litigant_cnt"
                           " from baseinfo01_cmp as bs LEFT JOIN dfnoticefeature01 AS sx "
                           " ON bs.company_name=sx.company_name where length(bs.company_name) >= 5 ")
    court_notice_feature.createOrReplaceTempView('court_notice_feature')

    # 合并基表誉法院公告, 法院公告开庭公告特征
    resdf = sqlContext.sql("select can.*,cno.court_notice_is_no,cno.court_notice_cnt,"
                           " cno.court_notice_litigant_cnt"
                           " from court_announce_feature can "
                           " LEFT JOIN court_notice_feature cno"
                           " ON can.company_name = cno.company_name")
    resdf.createOrReplaceTempView('court_feature')
    resdf.repartition(1).write.csv(os.path.join(savepath, "court_feature.csv"), mode='overwrite', header=True)
    sqlContext.sql("select * from court_feature sf WHERE sf.court_notice_cnt > 0").show()
    sqlContext.sql("select COUNT (*) from court_feature sf WHERE sf.court_notice_cnt > 0").show()


def feature_merge(spark, sc):
    '''
        吊销风险预测模型-特征合并
        被注销/吊销企业的数量 注销/吊销(labels_name.csv)
    1	在营（开业）企业
    2	吊销企业
    3	注销企业
    4	迁出
    8	停业
    9	其他
        :return:
    '''
    sqlContext = SQLContext(sparkContext=sc)
    sqlContext.registerFunction("empty_deal", lambda x: empty_deal(x))
    sqlContext.registerFunction("empty_deal_cnt", lambda x: empty_deal_cnt(x))
    sqlContext.registerFunction("cmp_years", lambda x: cmp_years(x))
    sqlContext.registerFunction("contains_String", lambda s0, s: contains_String(s0, s))

    label_mark = sqlContext.read.csv(Etlreadpath + 'labels_name.csv', header=False)
    label_mark.show()
    label_mark.createOrReplaceTempView('label_mark')
    sqlContext.sql("select count(1) from label_mark ").show()

    base_info = sqlContext.read.csv(Etlreadpath + 'base_info_name.csv',
                                    header=True)
    base_info.show()
    base_info.createOrReplaceTempView('baseinfo_cmp')

    sqlContext.sql("select count(1) from baseinfo_cmp ").show()

    # 法院公告 与 开庭公告
    court_feature = sqlContext.read.csv(feature_path + 'court_feature.csv',
                                   header=True)
    court_feature.createOrReplaceTempView('court_feature')
    print("法院公告 与 开庭公告")
    # sqlContext.sql("select count(1) from court_feature ").show()
    # court_feature.show()

    # 裁判文书
    judgedoc_feature = sqlContext.read.csv(feature_path + 'judgedoc_feature.csv',
                                   header=True)
    judgedoc_feature.createOrReplaceTempView('judgedoc_feature')
    print("裁判文书")
    # sqlContext.sql("select jf.*, lb._c1 as label from judgedoc_feature jf,label_mark lb WHERE jf.company_name=lb._c0")
    # judgedoc_feature.show()

    # 关联公司 裁判文书
    network_judgedoc_features = sqlContext.read.csv(feature_path + 'network_judgedoc_features',
                                   header=False)
    network_judgedoc_features.createOrReplaceTempView('network_judgedoc_features')
    print("关联公司 裁判文书")
    network_judgedoc_features.show()

    # 失信
    shixin_feature = sqlContext.read.csv(feature_path + 'shixin_feature.csv',
                                   header=True)
    shixin_feature.createOrReplaceTempView('shixin_feature')
    print("失信")
    ljtfeatures = sqlContext.sql("select jdf.*,njdf._c1 as net_judgedoc_defendant_cnt, "
                                 "  sxf.shixin_is_no, sxf.shixin_cnt, sxf.near_3_year_shixin_cnt, "
                                 "  sxf.near_2_year_shixin_cnt, sxf.near_1_year_shixin_cnt,"
                                 " cf.court_announce_is_no, cf.court_announce_cnt, cf.court_announce_litigant_cnt, "
                                 " cf.court_notice_is_no, cf.court_notice_cnt, cf.court_notice_litigant_cnt, "
                                   " lb._c1 as label "
                                 " from shixin_feature sxf,judgedoc_feature jdf,"
                                 " network_judgedoc_features njdf,court_feature cf,label_mark lb"
                   " WHERE sxf.company_name=jdf.company_name AND jdf.company_name=njdf._c0 "
                                 " and jdf.company_name=cf.company_name AND jdf.company_name =lb._c0")
    ljtfeatures.show()
    ljtfeatures.repartition(1).write.csv(os.path.join(savepath, "ljt_features.csv"), mode='overwrite', header=True)
    ljtfeatures.show()


def feature_merge_all(spark, sc):
    '''
        吊销风险预测模型-特征合并
        被注销/吊销企业的数量 注销/吊销(labels_name.csv)
    1	在营（开业）企业
    2	吊销企业
    3	注销企业
    4	迁出
    8	停业
    9	其他
        :return:
    '''
    sqlContext = SQLContext(sparkContext=sc)
    sqlContext.registerFunction("empty_deal", lambda x: empty_deal(x))
    sqlContext.registerFunction("empty_deal_cnt", lambda x: empty_deal_cnt(x))
    sqlContext.registerFunction("cmp_years", lambda x: cmp_years(x))
    sqlContext.registerFunction("contains_String", lambda s0, s: contains_String(s0, s))

    label_mark = sqlContext.read.csv(Etlreadpath + 'labels_name.csv', header=False)
    label_mark.show()
    label_mark.createOrReplaceTempView('label_mark')
    sqlContext.sql("select count(1) from label_mark ").show()
    print("new_ljt_features")
    dfl1 = sqlContext.read.csv(myfeature_path + 'new_ljt_features.csv', header=True)
    dfl1.show()
    dfl1.createOrReplaceTempView('new_ljt_features')
    sqlContext.sql("select count(1) from new_ljt_features ").show()
    print("hy_features")
    dfh1 = sqlContext.read.csv(myfeature_path + 'hy_features.csv', header=True)
    dfh1.show()
    dfh1.createOrReplaceTempView('hy_features')
    print("hy_features")
    dfc1 = sqlContext.read.csv(myfeature_path + 'ccs_features.csv', header=True)
    dfc1.show()
    dfc1.createOrReplaceTempView("ccs_features")
    sqlContext.sql("select count(1) from ccs_features ").show()


    ljtfeatures = sqlContext.sql("select  *  from new_ljt_features ljt,hy_features hy, ccs_features ccs"
                   " WHERE ccs.company_name=hy.company_name AND ccs.company_name=ljt.company_name "
                                )
    ljtfeatures.show()
    ljtfeatures.repartition(1).write.csv(os.path.join(savepath, "ljt_features.csv"), mode='overwrite', header=True)
    ljtfeatures.show()




def deal_label(d):

    if float(d) == 1.0:
        d = 0
    elif float(d) == 2.0:
        d = 1
    return d


def loss_sum_money(d):
    import math
    if isNone(d):
        d = 0
    else:
        try:
            d = float(d)
            if d < 0:
                d = abs(d)
                d = math.log(1 + d)
            else:
                d = 0
        except:
            d = 0
    return d

def industry_deal(data,code):
    '''
    空表示没有,非空表示有
    :param data:
    :return:
    '''
    if isNone(data):
        return 0
    else:
        try:
            data = int(data)
            if data == code:
                return 1
            else:
                return 0
        except:
            return 0



def feature_deal(spark, sc):
    '''
        吊销风险预测模型-特征合并
        被注销/吊销企业的数量 注销/吊销(labels_name.csv)
    1	在营（开业）企业
    2	吊销企业
    3	注销企业
    4	迁出
    8	停业
    9	其他
    处理后：
    1	吊销企业
    0   在营（开业）企业
        :return:
    '''
    sqlContext = SQLContext(sparkContext=sc)
    court_feature = sqlContext.read.csv(feature_path + 'all_features.csv',
                                   header=False)
    court_feature.createOrReplaceTempView('all_features')
    sqlContext.registerFunction("deal_label", lambda x: deal_label(x))
    sqlContext.registerFunction("empty_deal_cnt", lambda x: empty_deal_cnt(x))
    sqlContext.registerFunction("loss_sum_money", lambda x: loss_sum_money(x))
    sqlContext.registerFunction("industry_deal", lambda data, code: industry_deal(data, code))

    # sqlContext.sql("select  _c1, COUNT (1) from all_features GROUP BY _c1").show()
    '''
    13,0.381 棉、麻、糖、烟草种植
    26,0.254 化学原料和化学制品制造业
    519,0.246 其他批发业
    18,0.235 纺织服装、服饰业
    1810,0.204 机织服装制造
    62,0.195 褐煤开采洗选
    '''
    ljtfeatures = sqlContext.sql("select  empty_deal_cnt(_c1),  empty_deal_cnt( _c2),  empty_deal_cnt( _c3),  empty_deal_cnt( _c4),  empty_deal_cnt( _c5),  empty_deal_cnt( _c6),  "
                                 "empty_deal_cnt( _c7),  empty_deal_cnt( _c8),  empty_deal_cnt( _c9),  empty_deal_cnt(_c10),  empty_deal_cnt(_c11),  empty_deal_cnt(_c12),  "
                                 "empty_deal_cnt(_c13),  empty_deal_cnt(_c14),  empty_deal_cnt(_c15),  empty_deal_cnt(_c16),  empty_deal_cnt(_c17),  empty_deal_cnt(_c18),  empty_deal_cnt(_c19), "
                                 " empty_deal_cnt(_c20),  empty_deal_cnt(_c21),  empty_deal_cnt(_c22),  empty_deal_cnt(_c23),  empty_deal_cnt(_c24),  empty_deal_cnt(_c25), "
                                 "industry_deal(_c26,13) AS industry_13,industry_deal(_c26,26) AS industry_26,industry_deal(_c26,519) AS industry_519,industry_deal(_c26,18) AS industry_18, "
                                 "industry_deal(_c26,1810) AS industry_1810,"
                                 "industry_deal(_c26,62) AS industry_62,"
                                 "  empty_deal_cnt(_c30),  empty_deal_cnt(_c31),  empty_deal_cnt(_c32),  empty_deal_cnt(_c33),  empty_deal_cnt(_c34),  empty_deal_cnt(_c35), "
                                 " empty_deal_cnt(_c36),  empty_deal_cnt(_c37),  empty_deal_cnt(_c38),  empty_deal_cnt(_c39),  empty_deal_cnt(_c40),  empty_deal_cnt(_c41), "
                                 " empty_deal_cnt(_c42),  empty_deal_cnt(_c43),  empty_deal_cnt(_c44),  empty_deal_cnt(_c45),  empty_deal_cnt(_c46),  empty_deal_cnt(_c47), "
                                 " empty_deal_cnt(_c48),  empty_deal_cnt(_c49),  empty_deal_cnt(_c50),  empty_deal_cnt(_c51),  empty_deal_cnt(_c52),  empty_deal_cnt(_c53),  empty_deal_cnt(_c54),  "
                                 " empty_deal_cnt(_c55),  empty_deal_cnt(_c56),  empty_deal_cnt(_c57),  empty_deal_cnt(_c58),  empty_deal_cnt(_c59),  empty_deal_cnt(_c60),  empty_deal_cnt(_c61), "
                                 " empty_deal_cnt(_c62),  empty_deal_cnt(_c63),  empty_deal_cnt(_c64),  empty_deal_cnt(_c65)  "
                   " from all_features")
    ljtfeatures.show()
    ljtfeatures.repartition(1).write.csv(os.path.join(savepath, "data_dx2_zc02.csv"), mode='overwrite', header=False)
    ljtfeatures.show()
    # ljtfeatures1 = sqlContext.sql(
    #     "select  empty_deal_cnt(_c1),  empty_deal_cnt( _c2),  empty_deal_cnt( _c3),  empty_deal_cnt( _c4),  empty_deal_cnt( _c5),  empty_deal_cnt( _c6),  empty_deal_cnt( _c7),  empty_deal_cnt( _c8),  empty_deal_cnt( _c9),  empty_deal_cnt(_c10),  empty_deal_cnt(_c11),  empty_deal_cnt(_c12),  empty_deal_cnt(_c13),  empty_deal_cnt(_c14),  empty_deal_cnt(_c15),  empty_deal_cnt(_c16),  empty_deal_cnt(_c17),  empty_deal_cnt(_c18),  empty_deal_cnt(_c19),  empty_deal_cnt(_c20),  empty_deal_cnt(_c21),  empty_deal_cnt(_c22),  empty_deal_cnt(_c23),  empty_deal_cnt(_c24),  empty_deal_cnt(_c25),  empty_deal_cnt(_c26),  empty_deal_cnt(_c27),          empty_deal_cnt(_c28),  empty_deal_cnt(_c29),  empty_deal_cnt(_c30),  empty_deal_cnt(_c31),  empty_deal_cnt(_c32),  empty_deal_cnt(_c33),  empty_deal_cnt(_c34),  empty_deal_cnt(_c35),  empty_deal_cnt(_c36),  empty_deal_cnt(_c37),  empty_deal_cnt(_c38),  empty_deal_cnt(_c39),  empty_deal_cnt(_c40),  empty_deal_cnt(_c41),  empty_deal_cnt(_c42),  empty_deal_cnt(_c43),  empty_deal_cnt(_c44),  empty_deal_cnt(_c45),  empty_deal_cnt(_c46),  empty_deal_cnt(_c47),  empty_deal_cnt(_c48),  empty_deal_cnt(_c49),  empty_deal_cnt(_c50),  empty_deal_cnt(_c51),  empty_deal_cnt(_c52),  empty_deal_cnt(_c53),  empty_deal_cnt(_c54),  empty_deal_cnt(_c55),  empty_deal_cnt(_c56),  empty_deal_cnt(_c57),  empty_deal_cnt(_c58),  empty_deal_cnt(_c59),  empty_deal_cnt(_c60),  empty_deal_cnt(_c61),  empty_deal_cnt(_c62),  empty_deal_cnt(_c63),  empty_deal_cnt(_c64),  empty_deal_cnt(_c65)  "
    #     " from all_features WHERE _c1=1")
    # ljtfeatures1.repartition(1).write.csv(os.path.join(savepath, "data_zc_1.csv"), mode='overwrite', header=False)
    # ljtfeatures1.show()

def industry_dx_rate_deal(dx_rate):
    '''
    空表示没有,非空表示有
    :param data:
    :return:
    '''
    if isNone(dx_rate):
        return 0.0001
    else:
        try:
            dx_rate = float(dx_rate)
            return dx_rate
        except:
            return 0.0001

def feature_add(spark, sc):
    '''
        吊销风险预测模型-特征合并
        被注销/吊销企业的数量 注销/吊销(labels_name.csv)
    1	在营（开业）企业
    2	吊销企业
    3	注销企业
    4	迁出
    8	停业
    9	其他
    处理后：
    1	吊销企业
    0   在营（开业）企业
        :return:
    '''
    sqlContext = SQLContext(sparkContext=sc)
    court_feature = sqlContext.read.csv(feature_path + 'all_features.csv',
                                   header=True)
    court_feature.createOrReplaceTempView('all_features')
    industry_dx_rate = sqlContext.read.csv(savepath + 'industry_dx_rate.csv',
                                   header=True)
    industry_dx_rate.createOrReplaceTempView('industry_dx_rate')
    industry_dx_rate = sqlContext.sql("select * from industry_dx_rate t WHERE FLOAT(t.all_cnt) >= 3239")
    industry_dx_rate.show()
    industry_dx_rate.createOrReplaceTempView('industry_dx')

    sqlContext.registerFunction("deal_label", lambda x: deal_label(x))
    sqlContext.registerFunction("empty_deal_cnt", lambda x: empty_deal_cnt(x))
    sqlContext.registerFunction("loss_sum_money", lambda x: loss_sum_money(x))
    sqlContext.registerFunction("industry_dx_rate_deal", lambda x: industry_dx_rate_deal(x))
    sqlContext.registerFunction("industry_deal", lambda data, code: industry_deal(data, code))

    '''
    13,0.381 棉、麻、糖、烟草种植
    26,0.254 化学原料和化学制品制造业
    519,0.246 其他批发业
    18,0.235 纺织服装、服饰业
    1810,0.204 机织服装制造
    62,0.195 褐煤开采洗选
    '''
    ljtfeatures = sqlContext.sql("select  empty_deal_cnt(_c1),  empty_deal_cnt( _c2),  empty_deal_cnt( _c3),  empty_deal_cnt( _c4),  empty_deal_cnt( _c5),  empty_deal_cnt( _c6),  "
                                 "empty_deal_cnt( _c7),  empty_deal_cnt( _c8),  empty_deal_cnt( _c9),  empty_deal_cnt(_c10),  empty_deal_cnt(_c11),  empty_deal_cnt(_c12),  "
                                 "empty_deal_cnt(_c13),  empty_deal_cnt(_c14),  empty_deal_cnt(_c15),  empty_deal_cnt(_c16),  empty_deal_cnt(_c17),  empty_deal_cnt(_c18),  empty_deal_cnt(_c19), "
                                 " empty_deal_cnt(_c20),  empty_deal_cnt(_c21),  empty_deal_cnt(_c22),  empty_deal_cnt(_c23),  empty_deal_cnt(_c24),  empty_deal_cnt(_c25), "
                                 "industry_deal(_c26,13) AS industry_13,industry_deal(_c26,26) AS industry_26,industry_deal(_c26,519) AS industry_519,industry_deal(_c26,18) AS industry_18, "
                                 "industry_deal(_c26,1810) AS industry_1810,"
                                 "industry_deal(_c26,62) AS industry_62,"
                                 "industry_dx_rate_deal(indx.dx_rate) AS industry_dx_rate,"
                                 "empty_deal_cnt(indx.dx_cnt) AS industry_dx_cnt,"
                                 "empty_deal_cnt(indx.all_cnt) AS industry_all_cnt,"
                                 "  empty_deal_cnt(_c30),  empty_deal_cnt(_c31),  empty_deal_cnt(_c32),  empty_deal_cnt(_c33),  empty_deal_cnt(_c34),  empty_deal_cnt(_c35), "
                                 " empty_deal_cnt(_c36),  empty_deal_cnt(_c37),  empty_deal_cnt(_c38),  empty_deal_cnt(_c39),  empty_deal_cnt(_c40),  empty_deal_cnt(_c41), "
                                 " empty_deal_cnt(_c42),  empty_deal_cnt(_c43),  empty_deal_cnt(_c44),  empty_deal_cnt(_c45),  empty_deal_cnt(_c46),  empty_deal_cnt(_c47), "
                                 " empty_deal_cnt(_c48),  empty_deal_cnt(_c49),  empty_deal_cnt(_c50),  empty_deal_cnt(_c51),  empty_deal_cnt(_c52),  empty_deal_cnt(_c53),  empty_deal_cnt(_c54),  "
                                 " empty_deal_cnt(_c55),  empty_deal_cnt(_c56),  empty_deal_cnt(_c57),  empty_deal_cnt(_c58),  empty_deal_cnt(_c59),  empty_deal_cnt(_c60),  empty_deal_cnt(_c61), "
                                 " empty_deal_cnt(_c62),  empty_deal_cnt(_c63),  empty_deal_cnt(_c64),  empty_deal_cnt(_c65)  "
                   " from all_features AS f LEFT JOIN industry_dx AS indx ON f._c26=indx.industry")
    ljtfeatures.show()
    ljtfeatures.repartition(1).write.csv(os.path.join(savepath, "data_dx2_zc03.csv"), mode='overwrite', header=False)
    ljtfeatures.show()
    # ljtfeatures1 = sqlContext.sql(
    #     "select  empty_deal_cnt(_c1),  empty_deal_cnt( _c2),  empty_deal_cnt( _c3),  empty_deal_cnt( _c4),  empty_deal_cnt( _c5),  empty_deal_cnt( _c6),  empty_deal_cnt( _c7),  empty_deal_cnt( _c8),  empty_deal_cnt( _c9),  empty_deal_cnt(_c10),  empty_deal_cnt(_c11),  empty_deal_cnt(_c12),  empty_deal_cnt(_c13),  empty_deal_cnt(_c14),  empty_deal_cnt(_c15),  empty_deal_cnt(_c16),  empty_deal_cnt(_c17),  empty_deal_cnt(_c18),  empty_deal_cnt(_c19),  empty_deal_cnt(_c20),  empty_deal_cnt(_c21),  empty_deal_cnt(_c22),  empty_deal_cnt(_c23),  empty_deal_cnt(_c24),  empty_deal_cnt(_c25),  empty_deal_cnt(_c26),  empty_deal_cnt(_c27),          empty_deal_cnt(_c28),  empty_deal_cnt(_c29),  empty_deal_cnt(_c30),  empty_deal_cnt(_c31),  empty_deal_cnt(_c32),  empty_deal_cnt(_c33),  empty_deal_cnt(_c34),  empty_deal_cnt(_c35),  empty_deal_cnt(_c36),  empty_deal_cnt(_c37),  empty_deal_cnt(_c38),  empty_deal_cnt(_c39),  empty_deal_cnt(_c40),  empty_deal_cnt(_c41),  empty_deal_cnt(_c42),  empty_deal_cnt(_c43),  empty_deal_cnt(_c44),  empty_deal_cnt(_c45),  empty_deal_cnt(_c46),  empty_deal_cnt(_c47),  empty_deal_cnt(_c48),  empty_deal_cnt(_c49),  empty_deal_cnt(_c50),  empty_deal_cnt(_c51),  empty_deal_cnt(_c52),  empty_deal_cnt(_c53),  empty_deal_cnt(_c54),  empty_deal_cnt(_c55),  empty_deal_cnt(_c56),  empty_deal_cnt(_c57),  empty_deal_cnt(_c58),  empty_deal_cnt(_c59),  empty_deal_cnt(_c60),  empty_deal_cnt(_c61),  empty_deal_cnt(_c62),  empty_deal_cnt(_c63),  empty_deal_cnt(_c64),  empty_deal_cnt(_c65)  "
    #     " from all_features WHERE _c1=1")
    # ljtfeatures1.repartition(1).write.csv(os.path.join(savepath, "data_zc_1.csv"), mode='overwrite', header=False)
    # ljtfeatures1.show()

def train_test_validation(spark, sc):
    sqlContext = SQLContext(sparkContext=sc)
    label_mark = sqlContext.read.csv(savepath + 'ljt_train_dx.csv', header=False)
    label_mark.show()
    label_mark.createOrReplaceTempView('ljt_train_dx')
    sqlContext.sql("select count(1) from ljt_train_dx  WHERE label=1 or label=2").show()

    base_info = sqlContext.read.csv(Etlreadpath + 'base_info_name.csv',
                                    header=True)
    base_info.show()
    base_info.createOrReplaceTempView('baseinfo_cmp')

    sqlContext.sql("select count(1) from baseinfo_cmp ").show()

def testRead(spark, sc, path, filename):
    '''
    1	在营（开业）企业
    2	吊销企业
    3	注销企业
    4	迁出
    8	停业
    9	其他

    :param spark:
    :param sc:
    :param path:
    :param filename:
    :return:
    '''
    sqlContext = SQLContext(sparkContext=sc)
    df = sqlContext.read.csv(path + filename,
                             header=True)
    # df.show()
    df.createOrReplaceTempView('temp')
    # sqlContext.registerFunction("FormateRow", lambda x: pycsv.getRowFormate(x))
    # sqlContext.registerFunction("name_clean", lambda x: pycsv.name_clean(x))
    # resdf = sqlContext.sql("select COUNT(1) from ( "
    #                        "select zczjbz  from temp AS t GROUP  BY  zczjbz) AS tt")
    # resdf.show()
    sqlContext.sql("select  * from temp t ").show()
    sqlContext.sql("select  COUNT (DISTINCT  _c0) from temp t WHERE t.zczjbz =156 or t.zczjbz =0").show()
    # sqlContext.sql("select *  from  temp t WHERE _c0 ='上海双田橡胶（集团）公司' ").show()

if __name__ == '__main__':
    spark = SparkSession.builder.master(sparkpath) \
        .appName("ljt_features_spark").getOrCreate()
    sc = spark.sparkContext
    # sc.addPyFile('pysparkCsvUtils.py')
    testRead(spark, sc, feature_path, filename='new_version_all_features.csv')
    # feature_extract_shixin(spark, sc)
    # feature_extract_judgedoc(spark, sc)
    # feature_extract_court(spark, sc)
    # feature_merge(spark, sc)
    # feature_merge_all(spark, sc)
    # feature_deal(spark, sc)
    # feature_add(spark, sc)