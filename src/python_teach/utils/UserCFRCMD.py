#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on  20171116
基于用户的协同过滤
@author: ljt
'''
import math
import time
import datetime
import csv
import sys
sys.path.append("..")
import pandas as pd
import heapq
import os
import numpy as np
import random
from decimal import Decimal as D
import Levenshtein as lvst
import json
from sklearn.neighbors import NearestNeighbors
from utils.commenutils import conn001,product_get, NormalizedData, cos_distance, writejson, get_txt_data,writeAppendJson
from scpy.logger import get_logger
logger = get_logger(__file__)
# CURRENT_PATH = os.path.dirname(__file__)
# if CURRENT_PATH:
# 	CURRENT_PATH = CURRENT_PATH + '/'

def isNone(d):
    return (d is None or d == 'None' or
            d == '?' or
            d == '' or
            d == 'NULL' or
            d == 'null')

def calcuteSimilar(frame, targetID, otherUserID):
    '''
    计算余弦相似度
    :param frame: 数据集
    :param targetID: 目标用户ID
    :param otherUserID: 其他用户ID
    :return: 相似度
    UserID, Age, Edu, career, marital, everyFee, houseSize,  ownVehicle, Rating
    '''
    v1 = [float(frame[frame['UserID'] == targetID]['Age'].values[0]),
          float(frame[frame['UserID'] == targetID]['Edu'].values[0]),
          float(frame[frame['UserID'] == targetID]['career'].values[0]),
          float(frame[frame['UserID'] == targetID]['marital'].values[0]),
          float(frame[frame['UserID'] == targetID]['everyFee'].values[0]),
          float(frame[frame['UserID'] == targetID]['houseSize'].values[0]),
          float(frame[frame['UserID'] == targetID]['ownVehicle'].values[0]),
          float(frame[frame['UserID'] == targetID]['Rating'].values[0])]

    v2 = [float(frame[frame['UserID'] == otherUserID]['Age'].values[0]),
          float(frame[frame['UserID'] == otherUserID]['Edu'].values[0]),
          float(frame[frame['UserID'] == otherUserID]['career'].values[0]),
          float(frame[frame['UserID'] == otherUserID]['marital'].values[0]),
          float(frame[frame['UserID'] == otherUserID]['everyFee'].values[0]),
          float(frame[frame['UserID'] == otherUserID]['houseSize'].values[0]),
          float(frame[frame['UserID'] == otherUserID]['ownVehicle'].values[0]),
          float(frame[frame['UserID'] == otherUserID]['Rating'].values[0])]
    similarity = cos_distance(v1=v1, v2=v2)
    return similarity


def calcuteUserSimilar(frame, targetID=1, TopN=10):
    '''
    计算targetID的用户与其他用户的相似度
    :return:相似度TopN Series
    '''
    X = frame.as_matrix(columns=['Age', 'Edu', 'career', 'marital', 'everyFee', 'houseSize', 'ownVehicle', 'Rating'])

    age =frame[frame['UserID'] == targetID]['Age']
    if age.values.size>0:
        age = float(age.values[0])
    else:
        age = 0.0
    Edu = frame[frame['UserID'] == targetID]['Edu']
    if Edu.values.size>0:
        Edu = float(Edu.values[0])
    else:
        Edu = 0.0
    career = frame[frame['UserID'] == targetID]['career']
    if career.values.size>0:
        career = float(career.values[0])
    else:
        career = 0.0
    marital = frame[frame['UserID'] == targetID]['marital']
    if marital.values.size>0:
        marital = float(marital.values[0])
    else:
        marital = 0.0
    everyFee = frame[frame['UserID'] == targetID]['everyFee']
    if everyFee.values.size>0:
        everyFee = float(everyFee.values[0])
    else:
        everyFee = 0.0
    houseSize = frame[frame['UserID'] == targetID]['houseSize']
    if houseSize.values.size>0:
        houseSize = float(houseSize.values[0])
    else:
        houseSize = 0.0
    ownVehicle = frame[frame['UserID'] == targetID]['ownVehicle']
    if ownVehicle.values.size>0:
        ownVehicle = float(ownVehicle.values[0])
    else:
        ownVehicle = 0.0
    Rating = frame[frame['UserID'] == targetID]['Rating']
    if Rating.values.size>0:
        Rating = float(Rating.values[0])
    else:
        Rating = 0.0
    user = [age, Edu, career, marital, everyFee, houseSize, ownVehicle, Rating]

    nbrs = NearestNeighbors(n_neighbors=TopN, algorithm='ball_tree').fit(X)
    distances, indices = nbrs.kneighbors([user])
    # otherUsersID = np.array(indices.reshape(TopN, 1), dtype=int).flatten()
    # otherUsersID = frame[frame['UserID'] != targetID]['UserID'].values.tolist()
    otherUsersID = indices[0].tolist()
    similarlist = 1.0 - distances.reshape(TopN, 1).flatten()
    # print similarlist
    similarSeries = pd.Series(similarlist, index=otherUsersID)  # Series

    return similarSeries


def calAllItemSimilar(product_feature_path, product_Similar_path):
    '''
    计算所有产品与其他产品的相似度
    :return:
    '''
    product_Similar = {}
    filename = product_feature_path
    frame = pd.read_csv(filename)
    ItemIdList = [i for i in set(frame['id'])]
    Itemsize = len(ItemIdList)
    for targetItem in ItemIdList:
        logger.info("targetItem==>"+str(targetItem))
        targetSimilarItem = calcuteItemSimilar(frame, targetItem, TopN=Itemsize)
        product_Similar.update({targetItem: targetSimilarItem})
    writejson(product_Similar_path, product_Similar)

def calOneItemSimilar( product_feature_path, product_Similar_path,targetproductID):
    '''
    计算当前产品与其他产品的相似度
    :return:
    '''
    product_Similar = {}
    frame = pd.read_csv(product_feature_path)
    ItemIdList = [i for i in set(frame['id'])]
    Itemsize = len(ItemIdList)
    targetSimilarItem = calcuteOneSimilar(frame, targetproductID, TopN=Itemsize)
    product_Similar.update({targetproductID: targetSimilarItem})
    if targetSimilarItem:
        writeAppendJson(product_Similar_path, product_Similar)
    return product_Similar[targetproductID]


def calcuteItemSimilar(frame, targetItem, TopN=30):
    '''
    计算targetID的产品与其他产品的相似度
    :return:相似度TopN Series
    '''

    # 除了目标产品外其他产品ID
    otherItemId = [i for i in set(frame['id']) if i != targetItem]
    # 相似度列表
    similarItemList = [calcItemSimilar(frame, targetItem, itemId) for itemId in otherItemId]

    similarItemTopN = heapq.nlargest(TopN, similarItemList, key=lambda s: s['similarity'])

    return similarItemTopN

def calcuteOneSimilar(frame, targetproductID, TopN=30):
    '''
    计算targetID的产品与其他产品的相似度
    :return:相似度TopN Series
    '''
    # 除了目标产品外其他产品ID
    otherItemId = [i for i in set(frame['id']) if i != targetproductID]
    sql01 = """
      SELECT tp.status,tp.id, tp.type,tp.single_cost as singleCost,tp.day as tripDays,tp.accommodation as accStandard,tp.diet as catering,
                      json_array_elements(array_to_json(tp.region)) as region,
                      tp.nature AS naturalSce,tp.culture AS culturalSce,tp.folk AS folkwaysSce
FROM product tp WHERE tp.status='USE' AND tp.id=%d LIMIT 1
       """%(int(targetproductID))
    targetItem = conn001.query_one_sql(sql=sql01)
    if targetItem:
        type = targetItem.get("type")
        if type:
            type = str(type)
        else:
            type = 0.0
        tripDays = targetItem.get("tripDays")
        if tripDays:
            tripDays = float(tripDays)
        else:
            tripDays = 0.0
        accStandard = targetItem.get("accStandard")
        if accStandard:
            accStandard = str(accStandard)
        else:
            accStandard = ''
        catering = targetItem.get("catering")
        if catering:
            catering = str(catering)
        else:
            catering = ''
        singleCost01 = targetItem.get("singleCost01")
        if isNone(singleCost01):
            singleCost01 = 0.0
        v2 = [
            float(tripDays),
            float(singleCost01)
        ]
        region = targetItem.get("region", u"")
        if isNone(region):
            region = ""
        else:
            region = str(region)
        naturalSce = targetItem.get("naturalSce")
        if naturalSce:
            naturalSce = str(naturalSce)
        else:
            naturalSce = ""
        culturalSce = targetItem.get("culturalSce")
        if culturalSce:
            culturalSce = str(culturalSce)
        else:
            culturalSce = ""
        folkwaysSce = targetItem.get("folkwaysSce")
        if folkwaysSce:
            folkwaysSce = str(folkwaysSce)
        else:
            folkwaysSce = ""
        item = [accStandard, type, catering,  region,  naturalSce, culturalSce, folkwaysSce]
    else:
        logger.error("数据库未查到产品=》》/;%s" % (str(targetproductID)))
        return []
    # 相似度列表
    similarItemList = [calcOneSimilar(frame, otherItem, v2, item) for otherItem in otherItemId]
    similarItemTopN = heapq.nlargest(TopN, similarItemList, key=lambda s: s['similarity'])
    return similarItemTopN


def calcItemSimilar(frame, targetItem, otherItem):
    tripDays = frame[frame['id'] == otherItem]['tripDays'].values[0]
    if isNone(tripDays):
        tripDays = 0
    singleCost = frame[frame['id'] == otherItem]['singleCost'].values[0]
    if isNone(singleCost):
        singleCost = 0.0
    v1 = [
        float(tripDays),
        float(singleCost)
        ]
    tripDays01 = frame[frame['id'] == targetItem]['tripDays'].values[0]
    if isNone(tripDays01):
        tripDays01 = 0.0
    singleCost01 = frame[frame['id'] == targetItem]['singleCost'].values[0]
    if singleCost01:
        singleCost01 = 0.0
    v2 = [
          float(tripDays01),
          float(singleCost01)
        ]
    other = [
        str(frame[frame['id'] == otherItem]['accStandard'].values[0]),
        str(frame[frame['id'] == otherItem]['type'].values[0]),
        str(frame[frame['id'] == otherItem]['catering'].values[0]),
        str(frame[frame['id'] == otherItem]['region'].values[0]),
        str(frame[frame['id'] == otherItem]['naturalSce'].values[0]),
        str(frame[frame['id'] == otherItem]['culturalSce'].values[0]),
        str(frame[frame['id'] == otherItem]['folkwaysSce'].values[0])]

    item = [
        str(frame[frame['id'] == targetItem]['type'].values[0]),
        str(frame[frame['id'] == targetItem]['region'].values[0]),
        str(frame[frame['id'] == targetItem]['accStandard'].values[0]),
        str(frame[frame['id'] == targetItem]['catering'].values[0]),
        str(frame[frame['id'] == targetItem]['naturalSce'].values[0]),
        str(frame[frame['id'] == targetItem]['culturalSce'].values[0]),
        str(frame[frame['id'] == targetItem]['folkwaysSce'].values[0])]

    rate01 = 0.0
    vsize = len(v1)
    for j in range(0, vsize - 1):
        if math.isnan(v1[j]):
            v1[j] = 0.0
        elif math.isnan(v2[j]):
            v2[j] = 0.0
    cosrate = cos_distance(v1=v1, v2=v2)
    Isize = len(item)
    for i in range(0, Isize - 1):
        rate01 += lvst.ratio(other[i], item[i])
    similarity = round((cosrate + float(rate01 / Isize)) / 2.0, 2)
    if math.isnan(similarity):
        similarity = 0.0

    return {
        "otherItem": otherItem,
        "similarity": similarity
    }

def calcOneSimilar(frame,otherItem, v2,item):
    tripDays = frame[frame['id'] == otherItem]['tripDays'].values[0]
    if isNone(tripDays):
        tripDays = 0
    singleCost = frame[frame['id'] == otherItem]['singleCost'].values[0]
    if isNone(singleCost):
        singleCost = 0.0
    v1 = [
        float(tripDays),
        float(singleCost)
    ]

    other = [
        str(frame[frame['id'] == otherItem]['accStandard'].values[0]),
        str(frame[frame['id'] == otherItem]['type'].values[0]),
        str(frame[frame['id'] == otherItem]['catering'].values[0]),
        str(frame[frame['id'] == otherItem]['region'].values[0]),
        str(frame[frame['id'] == otherItem]['naturalSce'].values[0]),
        str(frame[frame['id'] == otherItem]['culturalSce'].values[0]),
        str(frame[frame['id'] == otherItem]['folkwaysSce'].values[0])]

    rate01 = 0.0
    vsize = len(v1)
    for j in range(0, vsize - 1):
        if math.isnan(v1[j]):
            v1[j] = 0.0
        elif math.isnan(v2[j]):
            v2[j] = 0.0
    cosrate = cos_distance(v1=v1, v2=v2)
    Isize = len(item)
    for i in range(0, Isize - 1):
        rate01 += lvst.ratio(other[i], item[i])
    similarity = round((cosrate + float(rate01 / Isize)) / 2.0, 2)
    if math.isnan(similarity):
        similarity = 0.0

    return {
        "otherItem": otherItem,
        "similarity": similarity
    }


def calcuteInterest(frame, similarSeries, targetItemID):
    '''
    计算目标用户对目标物品的感兴趣程度
    :param frame: 数据
    :param similarSeries: 目标用户最相似的K个用户
    :param targetItemID: 目标物品
    :return:感兴趣程度
    '''
    similarUserID = similarSeries.index  # 和目标用户最相似的K个用户
    similarUsers = [frame[frame['UserID'] == i] for i in similarUserID]  # K个用户数据
    similarUserValues = similarSeries.values  # 用户和其他用户的兴趣相似度
    UserInstItem = []
    for u in similarUsers:  # 其他用户对物品的感兴趣程度
        if targetItemID in u['productID'].values:
            rate=u[u['productID'] == targetItemID]['Rating'].values[0]
            if rate >0.0:
                UserInstItem.append(rate)
    urate = 0.0
    if len(UserInstItem)>0:
        urate= sum(
            [UserInstItem[v] for v in range(len(UserInstItem))]) / len(UserInstItem)
    # print UserInstItem
    simuser = 0.0
    size = len(similarUserValues)
    if size > 0:
        for it01 in similarUserValues:
            simuser += float(it01)
        if simuser < 0.0:
            simuser = 0.0
        else:
            simuser= simuser/size
    # print simuser
    interest = float(simuser*5000/100.0) + (5000 / 100.0) *urate
    if interest < 0.0:
        interest = 0.0
    if isNone(targetItemID):
        return ""
    return {"match_degree": round(interest, 2), "productID": targetItemID}

def calcuteUserInterest(frame, similarity, userID):
    '''
    预测userID用户与目标产品的匹配程度
    :param frame:全量数据
    :param similarity:与目标产品相似的产品的用户userID
    :param userID:预测userID用户
    :return:该用户对其他产品的评分的均值的1/2.0+similarity/2.0
    '''
    rate_degree = 0.0
    UserIDList =list(frame['UserID'])
    usize = len(UserIDList)
    RatingList = list(frame['Rating'])
    userrateList = [RatingList[i] for i in range(0, usize-1) if UserIDList[i] == userID]
    for ritem in userrateList:
        rate_degree += float(ritem)
    if rate_degree:
        rate_degree = rate_degree/float(len(userrateList))
    rate_degree = round((rate_degree*50/100.0+similarity*50/100.0)*100.0, 2)
    return rate_degree

def recomendUser(csvpath, product_Similar_path, targetItemID, UserNum=10):
    '''
    计算推荐给targetItemID的用户的TopN物品
    :param csvpath: 数据路径
    :param targetItemID: 目标产品
    :param TopN:
    :return: TopN个物品及感兴趣程度
    '''
    # 读取数据
    frame = pd.read_csv(csvpath)
    # 获取最相似K个产品
    product_Similar = get_txt_data(product_Similar_path)
    product_SimilarList01 = []
    product_SimilarList = []
    RCMuserIDList = []
    for key in product_Similar:
        if key == targetItemID:
            product_SimilarList = product_Similar[key]
            break
    # 对最相似的产品感兴趣的用户
    userIDLists = []
    for item in product_SimilarList:
        otherItem = item.get("otherItem", u"")
        if isNone(otherItem):
            continue
        otherItem = str(otherItem)
        similarity = item.get("similarity", u"")
        userIDList = list(set(frame[frame['productID'] == otherItem]['UserID']))
        userIDLists.extend(userIDList)
    #获取用户对目标产品的兴趣度
    userIDLists = list(set(userIDLists))
    for userID in userIDLists:
        match_degree = calcuteUserInterest(frame, similarity, userID)
        try:
            match_degree = float(match_degree)
            if match_degree < 40:
                continue
        except Exception as e:
            logger.error(e)
            continue
        product_SimilarList01.append({
            "userID": userID,  # string, 用户ID
            "match_degree": match_degree  # int, 匹配度
        })
    del product_SimilarList
    if len(product_SimilarList01) <= 0:
        product_SimilarList = calOneItemSimilar(product_feature_path, product_Similar_path, targetItemID)
        if len(product_SimilarList)<=0:
            return []
        # 对最相似的产品感兴趣的用户
        for item in product_SimilarList:
            otherItem = item.get("otherItem", u"")
            similarity = item.get("similarity", u"")
            userIDList = list(set(frame[frame['productID'] == otherItem]['UserID']))
            # 获取用户对目标产品的兴趣度
            for userID in userIDList:
                match_degree = calcuteUserInterest(frame, similarity, userID)
                try:
                    match_degree = float(match_degree)
                    if match_degree < 40:
                        continue
                except Exception as e:
                    logger.error(e)
                    continue
                product_SimilarList01.append({
                    "userID": userID,  # string, 用户ID
                    "match_degree": match_degree  # int, 匹配度
                })
    similarItemTopN = sorted(product_SimilarList01, key=lambda k: k['match_degree'], reverse=True)
    # similarItemTopN = heapq.nlargest(UserNum, product_SimilarList01, key=lambda s: s['match_degree'])
    return similarItemTopN


def calcuteItem(csvpath, targetUserID=2, TopN=10):
    '''
    计算推荐给targetUserID的用户的TopN物品
    :param csvpath: 数据路径
    :param targetUserID: 目标用户
    :param TopN:
    :return: TopN个物品及感兴趣程度
    '''
    # 读取数据
    frame = pd.read_csv(csvpath)
    TopN = 10
    # 计算最相似K个用户
    similarSeries = calcuteUserSimilar(frame, targetUserID, TopN)
    if len(similarSeries.values) <= 0:
        return []
    # 目标用户感兴趣的物品
    userproductID = set(frame[frame['UserID'] == targetUserID]['productID'])
    # 其他用户感兴趣的物品
    otherproductID = set(frame[frame['UserID'] != targetUserID]['productID'])
    # 差集
    productID = list(userproductID ^ otherproductID)

    # 推荐
    topNlist = []
    interestList = [calcuteInterest(frame, similarSeries, product) for product in productID]
    for itm in interestList:
        if isNone(itm):
            continue
        topNlist.append(itm)
    interestList = sorted(topNlist, key=lambda k: k['match_degree'], reverse=True)
    # interestSeries = pd.Series(interestList, index=productID)
    # rcmpSeries = interestSeries.sort_values(ascending=False)
    return interestList  # TopN

def init_num_data(d):
    if isNone(d):
        return 0.0
    else:
        return float(d)

def NormalizedOneUser(userid):
    '''
    归一化处理：y=(x-minValue)/(maxValue-minValue)
    :return:
    '''
    user_product_rating_path = "../data01/user_product_rating.csv"
    Evaluate = [u"很差", u"较差", u"普通", u"较好", u"很好"]
    edus = [u"小学",u"初中",u"高中",u"中专",u"大专",u"本科", u"硕士", u"博士"]
    Occupation = [u'职业经理人',u'工程师', u'公务员', u'事业编制人员', u'教师', u'医生', u'警察',
                       u'律师', u'企业主', u'个体工商户', u'自由职业']
    sql = """
    SELECT  id from client u   WHERE u.id='"""+str(userid)+"""' AND u.status!='DELETED';
    """

    result = conn001.query_all_sql(sql)
    if isNone(result):
        return False
    else:
        user_product_rating_path = "../data01/user_product_rating.csv"
        NormalizedData(user_product_rating_path)
        product_get("../data01/product_feature.csv")
        return True

def Normalized(x,minValue,maxValue):
    # try:
    x = float(x)
    minValue = float(minValue)
    maxValue = float(maxValue)
    y = (D(x - minValue) / D(maxValue - minValue)).quantize(D("0.0000"))
    return str(y)

def get_item_result(csvpath, targetUserID=2, TopN=10):

    targetUserID = int(targetUserID)
    start = time.time()
    #  数据源，目标用户id，推荐产品数量
    dict01 = {
        "time": str(datetime.datetime.now()),
        "userId": targetUserID,
        "content": []  # 按匹配度从高到低排序
    }

    rcUserItem = calcuteItem(csvpath, targetUserID=targetUserID, TopN=TopN)
    if len(rcUserItem) <= 0:
        if NormalizedOneUser(targetUserID):
            rcUserItem = calcuteItem(csvpath, targetUserID=targetUserID, TopN=TopN)
        else:
            return dict01
        if len(rcUserItem) <= 0:
            return dict01

    dict01["content"] = rcUserItem
    # result = json.dumps(dict01)
    logger.info('Cost time: %f' % (time.time() - start))
    return dict01



def get_user_result(csvpath, product_Similar_path,targetproductID, TopN=10):
    start = time.time()
    #  数据源，目标用户id，推荐产品数量
    dict01 = {
        "time": str(datetime.datetime.now()),
        "productID": targetproductID,
        "content": []  # 按匹配度从高到低排序
    }
    content = recomendUser(csvpath, product_Similar_path, targetproductID, TopN)
    dict01["content"] = content
    # result = json.dumps(dict01)
    logger.info('Cost time: %f' % (time.time() - start))
    return dict01

if __name__ == '__main__':
    csvpath = "../data01/user_product_rating.csv"
    product_feature_path = "../data01/product_feature.csv"
    product_Similar_path = "../data01/product_Similar.json"

    start = time.time()
    # filename = "data01/product_feature.csv"
    # frame = pd.read_csv(filename)
    print get_item_result(csvpath=csvpath, targetUserID='2103', TopN=10)
    # print lvst.ratio("大洋洲,澳大利亚--,奥克兰-罗托鲁瓦-布里斯班-凯恩斯-墨尔本","大洋洲,新西兰-澳大利亚-,奥克兰-墨尔本-黄金海岸-凯恩斯-悉尼")
    #更新产品相似度
    # calAllItemSimilar(product_feature_path="../data01/product_feature.csv", product_Similar_path="../data01/product_Similar.json")
    print get_user_result(csvpath, product_Similar_path, targetproductID="312", TopN=200)
    print('Cost time: %f' % (time.time() - start))
