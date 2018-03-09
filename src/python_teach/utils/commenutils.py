#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
常用方法
Created on 2017年11月22日
@author: ljt
'''
from numpy import *  # 导入numpy的库函数
import numpy as np
import os
# from utils.mysqlutil import Mysql
from utils.pg_traval_util import PgUtil
import re
import csv
import datetime
import sys
import codecs
import json
import sys
sys.path.append("../")
from decimal import Decimal as D
from scpy.logger import get_logger



reload(sys)
sys.setdefaultencoding("utf-8")

logger = get_logger(__file__)

# CURRENT_PATH = os.path.dirname(__file__)
# if CURRENT_PATH:
#     CURRENT_PATH = CURRENT_PATH + "/"


conn001 = PgUtil()

def sort_list_of_dict(list_to_be_sorted, key, reverse=True):
    '''
    根据dict的某一key值排序， 支持整数形式以及string，
    例如根据date字段降序排列

     [ {'name':'Homer', 'age':39, 'date':'2016-04-20 11:16:44'}, {'name':'Bart', 'age':10,'date':'2016-04-20 11:16:45'},
                          {'name':'Bart', 'age':10,'date':'2016-04-21 11:16:45'}]
    -->
    [{"date": "2016-04-21 11:16:45", "age": 10, "name": "Bart"}, {"date": "2016-04-20 11:16:45", "age": 10, "name": "Bart"},
     {"date": "2016-04-20 11:16:44", "age": 39, "name": "Homer"}]

    :param list_to_be_sorted:
    :param key:
    :param reverse:
    :return:
    '''
    newlist = sorted(list_to_be_sorted, key=lambda k: k[key], reverse=reverse)
    return newlist


def str_to_datetime(str):
    '''三种常规时间格式统一转换成一种格式比如:
    (2018年8月8日, 2018/08/08 20:20, 2018-08-08 20:20) --> 2018-08-08  --> 2018'''
    time_format_with_day = re.compile(u'[1-9][0-9]{3}[-年/]?[01]?[0-9][-月/]?[0-3]?[0-9]日?')
    if str:
        str_transfor = str.replace("年", "-").replace("月", "-").replace("日", "").replace("/", "-")
        try:
            clear_time = re.findall(time_format_with_day, str_transfor)
            if clear_time:
                result = datetime.datetime.strptime(clear_time[0], "%Y-%m-%d").date().year
            else:
                result = ""
        except Exception, e:
            result = ""
        return result
    else:
        return ""


def StrToFloat(float_string):
    if not re.match(r"^[+-]?(?:0|[1-9]\d*)(\.\d+)?$", float_string):
        logger.warn("价格类型不对float_string" + float_string)
    try:
        return float(float_string)
    except:
        logger.warn("价格类型不对float_string" + float_string)


def MergeHost(resource_list, key):
    '''
    对嵌套list去重
    :param resource_list:
    :param key:
    :return:
    '''
    if resource_list and isinstance(resource_list, list):
        allResource = []
        allResource.append(resource_list[0])
        for dict in resource_list:
            # print len(l4)
            k = 0
            for item in allResource:
                # print 'item'
                if dict[key] != item[key]:
                    k = k + 1
                    # continue
                else:
                    break
                if k == len(allResource):
                    allResource.append(dict)
        taskhost = []
        for item in allResource:
            nativePlace = item[key]
            if cmp(nativePlace, "") == 0 or cmp(nativePlace, None) == 0 or cmp(nativePlace, "-") == 0:
                continue
            else:
                taskhost.append(item[key])
    else:
        return resource_list
    return taskhost

def repeatCountList(resource_list):
    '''
    对嵌套list去重,并计算重复数量
    :param resource_list:
    :param key:
    :return:
    '''

    if resource_list and isinstance(resource_list, list):
        rep = set(resource_list)
        allResource = []
        for item in rep:
            if cmp(item, 'None') == 0 or cmp(item, '') == 0:
                continue
            else:
                allResource.append({"item": item, "count": int(resource_list.count(item))})
        return allResource

def IDCardgetage(cardno):
    try:
        year = cardno[6:10]
        Today = datetime.date.today()
        nowYear = Today.year
        return int(nowYear) - int(year)
    except Exception as err:
        return ""


def DecimaToPercentage(d):
    try:

        return "%.1f%%" % (d * 100)

    except Exception as e:
        logger.error(e)
        return "0.0%"

# 获取txt数据
def get_txt_data(path):
    with codecs.open(path, 'r') as json_file:
        data = json.loads(json_file.read())
        return data

def writejson(path, data):
    '''
     保存清洗数据
    '''
    t1 = datetime.datetime.now()
    f = open(path, 'w')
    # 方式1，字典按keys顺序编码
    data_string = json.dumps(data, sort_keys=True, indent=2)

    f.write(data_string.decode('unicode_escape'))
    f.write('\n')  # write不会在自动行末加换行符，需要手动加上
    f.flush()
    f.close()

def writeAppendJson(path, data):
    '''
     追加写入json数据
    '''
    orignalData = get_txt_data(path)
    if isinstance(orignalData, dict):
        data = dict(orignalData.items() + data.items())
    f = open(path, 'w')
    # 方式1，字典按keys顺序编码
    data_string = json.dumps(data, sort_keys=True, indent=2)
    f.write(data_string.decode('unicode_escape'))
    f.write('\n')  # write不会在自动行末加换行符，需要手动加上
    f.flush()
    f.close()


def cos_distance(v1, v2):
    try:
        dot_product = 0.0
        normA = 0.0
        normB = 0.0
        for a, b in zip(v1, v2):
            dot_product += a * b
            normA += a ** 2
            normB += b ** 2
        if normA == 0.0 or normB == 0.0:
            return 0.0
        else:
# 于归一化：
# 因为余弦值的范围是 [-1,+1] ，相似度计算时一般需要把值归一化到 [0,1]，一般通过如下方式：
# sim = 0.5 + 0.5 * cosθ
            return 0.5 + 0.5 * (dot_product/ ((normA * normB) ** 0.5+1))
    except Exception as e:
        logger.error(e)
        return 0.0




def Normalized(x,minValue,maxValue):
    # try:
    x = float(x)
    minValue = float(minValue)
    maxValue = float(maxValue)
    y = (D(x - minValue) / D(maxValue - minValue)).quantize(D("0.0000"))
    return str(y)
    # except Exception as e:
    #     logger.error(e)
    #     return 0.0

def NormalizedData(user_product_rating_path):
    '''
    归一化处理：y=(x-minValue)/(maxValue-minValue)
    :return:
    '''
    Evaluate = [u"很差", u"较差", u"普通", u"较好", u"很好"]
    edus = [u"小学",u"初中",u"高中",u"中专",u"大专",u"本科", u"硕士", u"博士"]
    Occupation = [u'职业经理人',u'工程师', u'公务员', u'事业编制人员', u'教师', u'医生', u'警察',
                       u'律师', u'企业主', u'个体工商户', u'自由职业']
    sql = """
        select a.*, p.id AS productno from(
               SELECT bb.*,cc.housesize  FROM (
                                                SELECT u.id as UserID, u.id_no as IDcard, u.age as Age,
                                                       ((to_jsonb(a.identify)) -> 'baseInfo' ->> 'education')  as Edu,
                                                       ((to_jsonb(a.occupation)) -> 'occupation' ->> 'occupation')  as career,
                                                       ((to_jsonb(a.occupation)) -> 'occupation' ->> 'position')  as position,
                                                       ((to_jsonb(a.occupation)) -> 'occupation' ->> 'type')  as IDType,
                                                       ((to_jsonb(a.marriage)) -> 'baseInfo' ->> 'presentSituation')  as marital,
                                                       (json_array_elements(array_to_json(a.travel_record)) -> 'product' ->>'price') as everyFee,
                                                       (json_array_elements(array_to_json(a.travel_record)) -> 'product' ->>'productId')::bigint as  productID,
                                                       array_to_json(a.travel_record) as travel_record,
                                                       u.salary as income,
                                                       jsonb_array_length(a.fixed_assets -> 'car') as ownVehicle
                                                from    client u LEFT JOIN archive a on u.archive_id=a.id WHERE u.status!='DELETED'
                                              ) bb LEFT JOIN
                 (SELECT tt.id, sum(area::DOUBLE PRECISION) as housesize FROM  (
                                                                                 SELECT u.id, jsonb_array_elements(a.fixed_assets -> 'house') ->>'area' as area
                                                                                 from client u LEFT JOIN archive a on u.archive_id=a.id
                                                                               )tt WHERE area!=''
                 group by  tt.id)cc
                   ON  cc.id=bb.UserID ) a
  left join (select id from product where status = 'USE') p on a.productID = p.id;
        """
    result = conn001.query_all_sql(sql)
    user_product_rating = list(result)
    out = open(user_product_rating_path, "w")
    csv_writer = csv.writer(out, dialect="excel")
    csv_writer.writerow(
        ["IDcard", "UserID", "Age", "Edu", "career", "marital", "everyFee", "houseSize", "productID", "ownVehicle",
         "Rating"])
    user_product_rating_normal = []
    maxAge=100
    minAge=0
    maxEdu=8
    minEdu=0
    maxcareer=12
    mincareer=0
    user_product_rating_everyFee = sorted(user_product_rating, key=lambda k: init_num_data(k['everyfee']),
                                         reverse=True)
    maxeveryFee=user_product_rating_everyFee[0]["everyfee"]
    if isNone(maxeveryFee) or maxeveryFee <=0:
        maxeveryFee= 1.0
    user_product_rating_houseSize = sorted(user_product_rating, key=lambda k: init_num_data(k['housesize']),
                                         reverse=True)
    maxhouseSize=user_product_rating_houseSize[0]["housesize"]
    if isNone(maxhouseSize) or maxhouseSize <=0:
        maxhouseSize = 1.0
    minhouseSize=0
    user_product_rating_ownVehicle = sorted(user_product_rating, key=lambda k: init_num_data(k['ownvehicle']),
                                         reverse=True)
    maxownVehicle=user_product_rating_ownVehicle[0]["ownvehicle"]
    if isNone(maxownVehicle) or maxownVehicle <=0:
        maxownVehicle = 1.0

    for item02 in user_product_rating:
        IDcard = item02.get("idcard", u"")
        if IDcard:
            IDcard = str(IDcard)
        productID = item02.get("productno", u"")
        if productID:
            productID = str(productID)
        UserID = item02.get("userid", u"")
        if isNone(UserID):
            continue
        else:
            try:
                UserID = int(UserID)
                logger.info("NormalizedData UserID:==> "+str(UserID))
            except:
                continue
        Age = item02.get("age", u"0")
        if isNone(Age):
            Age= 0
        Age = Normalized(x=Age, minValue=0, maxValue=maxAge)
        career = item02.get("career", u"")
        if isNone(career):
            career = 0.0
        else:
            for ite in Occupation:
                if ite == career:
                    career = Normalized(x=Occupation.index(ite)+1, minValue=0, maxValue=11)
                    break

        Edu = item02.get("edu")
        if isNone(Edu):
            Edu = 0.0
        else:
            i = 1
            for ite in edus:
                i += 1
                if ite == Edu:
                    Edu = Normalized(x=i, minValue=0, maxValue=maxEdu)
                    break
        try:
            Edu=float(Edu)
        except:
            Edu = 0.0
        try:
            career = float(career)
        except:
            career = 0.0
        marital = item02.get("marital", u"")
        if marital == u'已婚':
            marital = 1
        else:
            marital = 0
        everyFee = item02.get("everyfee")
        if isNone(everyFee):
            everyFee=init_num_data(everyFee)

        everyFee = Normalized(x=everyFee, minValue=0, maxValue=maxeveryFee)
        houseSize = item02.get("housesize")
        if isNone(houseSize):
            houseSize = 0.0
        else:
            houseSize = float(houseSize)
        houseSize = Normalized(x=houseSize, minValue=0, maxValue=maxhouseSize)
        ownVehicle = item02.get("ownvehicle", u"0")
        if isNone(ownVehicle):
            ownVehicle = 0
        ownVehicle = Normalized(x=ownVehicle, minValue=0, maxValue=maxownVehicle)
        score = 0
        travel_record = item02.get("travel_record", [])
        if isinstance(travel_record, list):
            for item in travel_record:
                clientEvaluate = item.get("clientEvaluate", {})
                shopping = clientEvaluate.get("shopping", u"")
                if shopping:
                    if shopping in Evaluate:
                        score += Evaluate.index(shopping) + 1
                suggest = clientEvaluate.get("suggest", u"")
                if suggest:
                    if suggest in Evaluate:
                        score += Evaluate.index(suggest) + 1
                visit = clientEvaluate.get("visit", u"")
                if visit:
                    if visit in Evaluate:
                        score += Evaluate.index(visit) + 1
                leader = clientEvaluate.get("leader", u"")
                if leader:
                    if leader in Evaluate:
                        score += Evaluate.index(leader) + 1
                standard = clientEvaluate.get("standard", u"")
                if standard:
                    if standard in Evaluate:
                        score += Evaluate.index(standard) + 1
                guide = clientEvaluate.get("guide", u"")
                if guide:
                    if guide in Evaluate:
                        score += Evaluate.index(guide) + 1
                if score is not None and cmp(score, "") != 0:
                    score = int(score)
        Rating = score
        Rating = Normalized(x=Rating, minValue=0, maxValue=30)
        user_product_rating_normal.append({
            "IDcard": str(IDcard),
            "UserID": str(UserID),
            "Age": str(Age),
            "Edu": str(Edu),
            "career":str( career),
            "marital": str(marital),
            "everyFee": str(everyFee),
            "houseSize": str(houseSize),
            "productID": str(productID),
            "ownVehicle": str(ownVehicle),
            "Rating": str(Rating)
        })
        csv_writer.writerow(
            [str(IDcard), int(UserID), str(Age), str(Edu), str(career), str(marital), str(everyFee),
                                                                                    str(houseSize), str(productID), str(ownVehicle), str(Rating)])
    out.close()

def init_num_data(d):
    if isNone(d):
        return 0.0
    else:
        return float(d)

def product_get(product_feature_path):
    out = open(product_feature_path, "w")
    csv_writer = csv.writer(out, dialect="excel")
    csv_writer.writerow(
        ["id", "type", "singleCost", "tripDays", "accStandard", "catering",
          "region", "naturalSce", "culturalSce", "folkwaysSce"])
    sql = """
    SELECT tp.status,tp.id, tp.type,tp.single_cost as singleCost,tp.day as tripDays,tp.accommodation as accStandard,tp.diet as catering,
                      tp.region::TEXT as region,
                      tp.nature AS naturalSce,tp.culture AS culturalSce,tp.folk AS folkwaysSce
FROM product tp WHERE tp.status='USE'
  """
    result = conn001.query_all_sql(sql)
    result = list(result)
    for item in result:
        # print item
        id = item.get("id", u"")
        type = item.get("type", u"")
        singleCost = item.get("singlecost", u"")
        tripDays = item.get("tripdays", u"")
        accStandard = item.get("accstandard", u"")
        catering = item.get("catering", u"")
        region = item.get("region", u"")
        naturalSce = item.get("naturalsce", u"")
        culturalSce = item.get("culturalsce", u"")
        folkwaysSce = item.get("folkwayssce", u"")
        csv_writer.writerow(
            [str(id), str(type), str(singleCost), str(tripDays), str(accStandard), str(catering),
                                      str(region), str(naturalSce), str(culturalSce), str(folkwaysSce)])
    out.close()

def isNone(d):
    return (d is None or d == 'None' or
            d == '?' or
            d == '' or
            d == 'NULL' or
            d == 'null')

def return_format(d):
    if isNone(d):
        return '--'
    else:
        return str(d)


if __name__ == "__main__":
    #
    # v1 = [0.000256, 0.0004, 0.000129, 0.07249]
    # v2 = [0.000972, 0.0139, 0.00207, 0.05858]
    # print cos_distance(v1, v2)
    user_product_rating_path = "../data01/user_product_rating.csv"
    NormalizedData(user_product_rating_path)
    product_get("../data01/product_feature.csv")