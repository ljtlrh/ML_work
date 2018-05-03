redis:
redis-cli -h 127.0.0.1 -p 6379 -a 123456
hadoop:
/home/sinly/ljtstudy/hadoop
neo4j
sinly@sinly-All-Series:~/ljtstudy/neo4j-community-3.2.6/bin$ ./neo4j console

127.0.0.1:7687

/opt/spark/python/lib
/opt/spark/python/:/opt/spark/python/lib/py4j-0.10.3-src.zip:/usr/bin/python2.7
服务器地址：192.168.31.10
用户名 scdata
密码 scmodel2015
hadoop集群管理地址:
http://192.168.31.10:8088/cluster
hdfs存储管理:
http://192.168.31.10:50070
python+pyspark:
http://blog.csdn.net/weiyudang11/article/details/51841413
http://192.168.31.10:8080
/home/scdata/app/python/risk-model/etl_ljt_script

数据所在的目录　/home/scdata/riskModelData
同时hdfs也存入同样的数据 /scdata/riskModel/riskModelData

除工商数据外，其他数据均从爬虫数据库导出

python 版本示例
test.py :
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[10]").appName("understanding_sparksession").getOrCreate()
df = spark.read.csv('hdfs://192.168.31.10:9000/scdata/riskModel/riskModelData/basic_info.csv', header=True)
res = spark.sql("select * from temp limit 100")
res.show()

使用spark-submit执行py脚本
spark-submit --master spark://192.168.31.10:7077 --executor-memory 120G --total-executor-cores 35 /home/scdata/app/python/risk-model/etl_ljt_script/SC_ETL01.py

删除:
 hadoop fs -rm -f -R  /scdata/riskModel/features/ljt_train_data.txt

上传:
scp ./SC_ETL01.py  scdata@192.168.31.10:~/app/python/risk-model/etl_ljt_script/

下载:
hadoop fs -getmerge hdfs://192.168.31.10:9000/scdata/riskModel/update_trade_cnt_feature_data.csv update_trade_cnt_feature_data.csv
hadoop fs -getmerge hdfs://192.168.31.10:9000/scdata/riskModel/new_update_LGBM_model_test_data.csv LGBM_model_test.csv
hadoop fs -getmerge hdfs://192.168.31.10:9000/scdata/riskModel/new_version_all_features.csv new_version_all_features.csv
注：提取数据时的sql语句

--执行

select court_zhixing_new.company_name,court_zhixing_new.sc_data_id, court_zhixing_new.case_create_time, court_zhixing_new.execute_money,
court_zb.end_time
from court_zhixing_new left join court_zb on court_zhixing_new.case_code = court_zb.case_code and court_zhixing_new.company_name =  court_zb."name"


--失信
select company_name, sc_data_id, publish_date, reg_date from court_shixin_company_new

-- 行政处罚
select case_name, sc_data_id, punish_type, publish_date from punish

-- 网贷黑名单
select company_name, sc_id as sc_data_id, problem_time, event_type, platform_name from p2p_black_list

-- 裁判文书
select judgedoc_litigant.litigant_name, judgedoc_litigant.doc_id as sc_data_id, judgedoc_litigant.litigant_type, judgedoc.case_type, judgedoc.case_reason,
judgedoc.publish_date, judgedoc.trail_date,judgedoc.case_result  from
judgedoc_litigant left join judgedoc on  judgedoc_litigant.doc_id =  judgedoc.doc_id

--开庭公告

select sc_courtannouncement_litigant.litigant_name, sc_courtannouncement.sc_data_id, sc_courtannouncement_litigant.litigant_type,
sc_courtannouncement.case_reason, sc_courtannouncement.case_type,sc_courtannouncement.publish_time, sc_courtannouncement.judge_time
from sc_courtannouncement_litigant left join sc_courtannouncement on sc_courtannouncement_litigant.announcement_id = sc_courtannouncement.sc_data_id

-- 法院公告
select sc_courtnotice_litigant.litigant_name, sc_courtnotice_litigant.litigant_type,
sc_courtnotice.sc_data_id, sc_courtnotice.case_reason, sc_courtnotice.case_type,sc_courtnotice.publish_time
from sc_courtnotice_litigant left join sc_courtnotice on
sc_courtnotice_litigant.notice_id = sc_courtnotice.sc_data_id


--司法拍卖
select court_sszc_crawl_company.company_name, court_sszc_crawl_company.sc_data_id, court_sszc_crawl.min_price, court_sszc_crawl.common_price, court_sszc_crawl.sell_price,
court_sszc_crawl.publish_date, court_sszc_crawl.asset_type from court_sszc_crawl_company left join court_sszc_crawl
on  court_sszc_crawl.sc_data_id = court_sszc_crawl_company.sc_data_id

--专利

select apply_person, sc_id as sc_data_id , type, apply_date, authorize_publish_date from company_patent

--商标
select company_name, sc_data_id, int_type_code,pre_publication_time,apply_time,reg_publication_time from trademark

