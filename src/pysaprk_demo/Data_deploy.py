#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 2018/3/21 15:50
# @Author  : liujiantao
# @Site    : PySpark处理数据并图表分析 https://blog.csdn.net/u011204847/article/details/51224383
# @File    : Data_deploy.py
# @Software: PyCharm
from __future__ import print_function
from pyspark import SparkConf, SparkContext
from pyspark.mllib.clustering import KMeans
from pyspark.sql import SparkSession
hdfspath = 'hdfs://localhost:9000'
ml_100k = hdfspath + '/train/ml-100k/'
sparkpath = "local[2]"

def test01():
    from pyspark import SparkContext
    # conf = SparkConf().setMaster("local").setAppName("Test")
    # sc = SparkContext(conf)
    sc = SparkContext("local[2]", "First Spark App")
    user_df = sc.textFile(ml_100k+"u.user")
    first = user_df.first()
    print(first)

def test02():
    from pyspark import SparkContext
    sc = SparkContext("local", "Job Name", pyFiles=['MyFile.py', 'lib.zip', 'app.egg'])
    words = sc.textFile("/usr/share/dict/words")
    words.filter(lambda w: w.startswith("spar")).take(5)

def test03():
    """
    处理一（用户年龄统计分析）
    处理一简介：
    通过对用户数据处理，获得用户信息中的年龄。然后对年龄进行统计并使用Python中的图形框架Matplotlib生成柱状图，最后通过柱状图分析观看电影的观众年龄分布趋势。
    :return:
    """
    sc = SparkContext("local[2]", "First Spark App")
    # 加载HDFS上面的用户数据
    user_data = sc.textFile(ml_100k+"u.user")
    # 打印加载的用户信息第一条
    user_data.first()
    # KMeans.train()

    # 用"|"分割符分割每一行的数据，然后将数据返回到user_fields
    user_fields = user_data.map(lambda line: line.split("|"))
    # 统计总的用户数
    num_users = user_fields.map(lambda fields: fields[0]).count()
    # 统计性别的种类数，distinct()函数用来去重。
    num_genders = user_fields.map(lambda fields: fields[2]).distinct().count()
    # 统计职位种类数
    num_occupations = user_fields.map(lambda fields: fields[3]).distinct().count()
    # 统计邮政编码种类数
    num_zipcodes = user_fields.map(lambda fields: fields[4]).distinct().count()
    # 打印统计的这些信息
    print("Users: %d, genders: %d, occupations: %d, ZIP codes: %d"
          % (num_users, num_genders, num_occupations, num_zipcodes))

    # 统计用户年龄
    ages = user_fields.map(lambda x: int(x[1])).collect()
    # 通过python中的matplotlib生成图表提供给分析师分析
    import matplotlib.pyplot as plt
    plt.hist(ages, bins=20, color='lightblue', normed=True)
    fig = plt.gcf()
    fig.set_size_inches(16, 10)
    plt.show()

def test04():
    spark = SparkSession.builder.master(sparkpath) \
        .appName("ETL_ljt_spark").getOrCreate()
    sc = spark.sparkContext
    # sc.addPyFile('pysparkCsvUtils.py')
    # sc.addPyFile('caseReasonCode.py')
    # sc.addPyFile('case_reason_reflection.py')
    # sc.addPyFile('case_reason_map.py')
    # sc.addPyFile('parser.py')
    # sc.addPyFile('judgedoc.model.bin')
    spark.stop()

if __name__ == '__main__':
    # spark = SparkSession.builder.master("local") \
    #     .appName("SparkUserData").getOrCreate()
    # sc = SparkContext("local[2]", "First Spark App")
    # sc = spark.sparkContext
    # test01()
    # test03()
    test04()