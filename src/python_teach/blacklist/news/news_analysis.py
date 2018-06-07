# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import json
import sys

import requests
from flask import Flask, request
from scpy.logger import get_logger

logger = get_logger(__file__)

app = Flask(__name__)
reload(sys)
sys.setdefaultencoding('utf8')

import base64
import boto3


S3 = boto3.resource('s3')

# NEWS_CONTENT_IP = '172.31.7.180:18080'
# STRAT_IP = '172.31.8.30:7000'


NEWS_CONTENT_IP = '52.80.98.74:18080'
STRAT_IP = '52.80.91.161:7000'

# 最少出现次数
match_threshold = 0

# 表示否定的词
neg = re.compile(u"未|无|不存在|否|没|并非|扭转|扭亏|缓解|摆脱|弥补|收回|回收|追回|兑现|拒绝|被拒|改善|偿还|消除|解决|好转|"
                 u"逆转|蜕变|不会有|造谣|否认|补偿|归还|不拖欠|增长|谣言|翻身|止住|不像|抵|帮助|催收|还款")

# 表示假设/以前发生的词
uncertain = re.compile(u"将要|可能|如果|预测|猜测|预计|或|表示|年前|当初|前身|当年")

# 长句（报表）中用来分句的词 i.e.（1）／ 1、／（一）／一、
num = u"(\d、)|(（\d）)|((一|二|三|四|五|六|七|八|九|十)、)|(（(一|二|三|四|五|六|七|八|九|十)）)"

# 规则
rules = {
	0: u"((资金|款).{0,4}(短缺|非法|断裂|挪用|逾期|延迟|不足|危机|紧张))|((非法|欠|挪用|逾期|延迟|不足).{0,4}(资金|款))",
	1: u"(破产|倒闭|关闭|关门|亏损|闹事|盲目扩张|积压|滞后|下滑|下降|薄弱|缩水|停工|停产|停业|不正当竞争|欠缴)",
	2: u"((破产|倒闭).{0,4}(清算|申请|宣布|濒临|启动))|((清算|申请|宣布|濒临|启动).{0,4}(破产|倒闭))",
	3: u"((亏损).{0,5}(出现|导致|发生|继续|持续|万|亿|元))|((出现|导致|发生|继续|持续|((万|亿|元).{0,3}的)).{0,5}(亏损))",
	4: u"(拖|欠).{0,5}(货|款)",
	5: u"((裁员).{0,5}(大幅|大量|正在|持续|不断|宣布))|((大幅|大量|正在|持续|不断|宣布).{0,5}(裁员))",
	6: u"((资金|财产|资产|账户|存款).{0,5}(冻结|查封|扣押))|((冻结|查封|扣押).{0,5}(资金|财产|资产|账户|存款))",
	7: u"(拖|欠|迟|延|不支付).{0,5}(薪酬|工资|劳动报酬)",
	8: u"((财务).{0,5}(存疑|失实|造假|欺诈))|((存疑|失实|造假|欺诈).{0,5}(财务))",
	9: u"((经营|盈利).{0,5}(困难|停止|堪忧|恶化|亏损|慢|下滑|少))|(停止.{0,5}(经营|盈利))",
	10: u"((收购).{0,10}(失败))|((失败).{0,10}(收购))"
}

# 风险词汇
risks = [
	"停止销售并召回",
	"高管宣布离职",
	"财务数据真实性存疑",
	"公司倒闭",
	"高管欠薪跑路",
	"拖欠劳动报酬",
	"财务真实性存疑",
	"产品不合格",
	"濒临倒闭",
	"申请破产",
	"跑路传言",
	"涉嫌自融",
	"虚报利润",
	"董事会主席侵吞公司财产",
	"涉嫌非法集资",
	"公司破产",
	"连续亏损",
	"供应商讨债",
	"非法吸收公众存款",
	"卷款跑路",
	"资金问题停工",
	"大幅裁员",
	"虚假宣传处罚",
	"收购失败",
	"拖欠工人工资",
	"巨额亏损",
	"庞氏骗局",
	"产品缺陷",
	"携款潜逃",
	"公司停产整治",
	"高管离职",
	"不支付劳动报酬",
	"产品召回",
	"陷入资金危机",
	"高管集体离职",
	"财务处理不当",
	"财务数据失实",
	"裁员资金链断裂",
	"破产清算",
	"涉嫌财务欺诈",
	"高管携款潜逃",
	"资不抵债",
	"资金链问题",
	"公司违规",
	"劳动仲裁",
	"高管辞职",
	"拖欠员工工资",
	"产品责任纠纷",
	"跑路事件",
	"流动资金不足",
	"持续经营能力遭质疑",
	"恶意欠薪",
	"高管接连离职",
	"经营状况持续恶化",
	"高层的人事变动",
	"资产冻结",
	"宣布破产",
	"高管请辞",
	"涉嫌财务造假",
	"欠缴金额",
	"跌停",
	"涉嫌违规",
	"房产被抵押",
	"被最高法列入失信公司名单",
	"被列入失信名单",
	"净亏损",
	"CEO离职",
	"CTO离职",
	"未及时披露重大关联交易",
	"予以监管关注",
	"披露不及时",
	"(被告二)",
	"(被告一)",
	"可能被暂停上市",
	"净利润继续为负值",
	"净利润为负",
	"诉至法院",
	"较大金额亏损",
	"较大金额的亏损"
]


# 将风险词汇加入规则
def initKeywords():
	keyword = ""
	for kw in risks:
		keyword += kw.encode("utf8") + "|"
	rules[11] = u'(' + keyword[:-1] + u')'


initKeywords()

def new_strategy_types(strategy_keys):
	strategies = {}
	for key in strategy_keys:
		for pair in key:
			if len(pair) != 2:
				# print 'history company name:', type(key), key
				temp = strategies.get(key['keyType'], [])
				if key['keyValue'] not in temp:
					temp.append(key['keyValue'])
					strategies[key['keyType']] = temp
			else:
				temp = strategies.get(pair['keyType'], [])
				if pair['keyValue'] not in temp:
					temp.append(pair['keyValue'])
					strategies[pair['keyType']] = temp
	return strategies


def checkContent(url, content, strategies):
	if not content:
		return {"hit": False, "url": "", "hitResults": []}

	# 根据公司的抓取策略获取公司信息
	# 将keyword（暂未使用historyKeyword或historyCompany）转为regex
	# print 'Extracting key words'
	if not strategies:
		logger.warn('No strategies provided.')
		return {"hit": False, "url": url, "hitResults": []}
	names = strategies.get('company', [])
	if "keyword" in strategies.keys():
		names += strategies["keyword"]
	# if "historyKeyword" in strategies.keys():
	#     names += strategies["historyKeyword"]
	# if "historyCompany" in strategies.keys():
	#     names += strategies["historyCompany"]
	comp_name = ""
	for name in names:
		comp_name += name + "|"
	# logger.info('possible company names includes: %s %s ' % (type(comp_name[:-1]), comp_name[:-1]))


	names = re.compile(comp_name[:-1].decode('utf8'))

	cur_rules = rules.copy()

	if names:
		cur_rules[len(cur_rules)] = u'(' + comp_name[:-1] + u").{0,40}" + rules[11]

	# 将product, frName, keyMember加入规则
	if "product" in strategies.keys():
		products = ""
		for product in strategies["product"]:
			products += product + "|"
		# logger.info('company products are: %s' % products[:-1])
		rule_12 = "((" + products[:-1] + u").{0,5}(不合格|停止销售|召回|缺陷))|" \
		                                 u"((不合格|停止销售|召回|缺陷).{0,5}(" + products[:-1] + "))"
		cur_rules[len(cur_rules)] = rule_12

	if "frName" in strategies.keys():
		fr = ""
		surnames = []
		for cur_fr in strategies["frName"]:
			fr += cur_fr + "|"
			if cur_fr[0] not in surnames:
				fr += cur_fr[0] + "(某|先生|女士|小姐)|"
				surnames.append(cur_fr[0])
		# logger.info('company corporates are: %s' % fr[:-1])
		rule_13 = u"((" + fr[:-1] + u").{0,5}(跑路|跑到|失联|人去楼空|逃|卷款|藏匿|携款|出走))|" \
		                            u"((跑路|跑到|失联|人去楼空|逃|卷款|藏匿|携款|出走).{0,5}(" + fr[:-1] + "))"
		cur_rules[len(cur_rules)] = rule_13


	if "keyMember" in strategies.keys():
		members = ""
		member_surnames = []
		for member in strategies["keyMember"]:
			members += member + "|"
			if member[0] not in member_surnames:
				members += member[0] + "(某|先生|女士|小姐)|"
				member_surnames.append(member[0])
		# logger.info('company key members are: %s' % members[:-1])
		rule_14 = "((" + members[:-1] + u")+.{0,5}(离职|辞去|辞职|请辞))|((离职|辞去|辞职|请辞).{0,5}(" + members[:-1] + "))"
		cur_rules[len(cur_rules)] = rule_14

	# logger.info('CONTAINING %s RULES IN TOTAL / %s' % (len(cur_rules), len(rules)))

	# 判断是否为银行，如果是，则跳过规则6
	bank = re.compile(u"银行").search(comp_name[:-1])
	results = checkRules(content, names, cur_rules, bank)
	if results:
		return {"hit": True, "url": url, "hitResults": results}
	return {"hit": False, "url": url, "hitResults": results}


def getStrategy(company_name):
	# print 'Getting Strategies'
	r = requests.get('http://%s/api/news/strategy' % STRAT_IP, params={'name': company_name})
	return r.json()


def checkRules(sentences, names, cur_rules, bank):
	# 分句（标点符号）
	data = re.split(u"[。！？]", sentences)
	# print data
	hit_results = []
	# 对规则12做检查,即公司名称后30个字内容有关键词risks定义的内容
	rule = re.compile(cur_rules.get(12))
	for sentence in data:
		if rule.search(sentence):
			hit_result = {}
			hit_result["hitSentence"] = sentence
			hit_result["rule"] = cur_rules.get(12)
			hit_results.append(hit_result)
			return hit_results
	# 将除0，1外的所有规则转为regex，对于每个规则，判断是否有句子符合符合规则
	for x in range(2, len(cur_rules)):
		if x == 6:
			if bank:
				# SKIP RULE 6 FOR BANKS
				continue
		rule = re.compile(cur_rules.get(x))
		# print 'checking rule_', count, '; finding ', len(rule.findall(sentences)), ' existence'
		if len(rule.findall(sentences)) > match_threshold:
			# print 'finding rule_', x, ' with ', len(rule.findall(sentences)), ' existence'
			# logger.info('finding rule %s with %s  existence' % (x, len(rule.findall(sentences))))

			for sentence in data:
				# 如果符合规则，判断该句是否出现过否定词或假设词
				if rule.search(sentence):
					hit_result = False
					# if the sentence is too long. i.e. reports with data
					if len(sentence) > 200 and re.compile(num).search(sentence):
						# print 'split the sentence', len(sentence)
						for target in re.split(num, sentence):
							if target:
								hit_result = ruleCheckNeg(target, names, rule)
								if hit_result:
									break
					else:
						# print sentence
						hit_result = ruleCheckNeg(sentence, names, rule)

					# 如果命中，加入hit_results
					if hit_result:
						# print '!!!!!!HIIIIIIIIT: ', sentence, "\n"
						hit_result["hitSentence"] = sentence
						hit_result["rule"] = cur_rules.get(x)
						hit_results.append(hit_result)

	# Rule 0&1
	temp_results = []
	index = 0
	for pattern in [re.compile(cur_rules.get(0)), re.compile(cur_rules.get(1))]:
		if len(pattern.findall(sentences)) > 0:
			# logger.info('finding rule %s with %s  existence' % (index, len(pattern.findall(sentences))))
			for sentence in data:
				if pattern.search(sentence):
					hit_result = False
					# if the sentence is too long. i.e. reports with data
					if len(sentence) > 200 and re.compile(num).search(sentence):
						# print 'split the sentence', len(sentence)
						for target in re.split(num, sentence):
							if target:
								hit_result = ruleCheckNeg(target, names, pattern)
								if hit_result:
									break
					else:
						# print sentence
						hit_result = ruleCheckNeg(sentence, names, pattern)
					if hit_result:
						# print '!!!!!!HIIIIIIIIT: ', sentence, "\n"
						hit_result["hitSentence"] = sentence
						hit_result["rule"] = cur_rules.get(index)
						temp_results.append(hit_result)
		index += 1

	# Rule 0&1的命中次数 >= 2才加入hit_results
	if len(temp_results) > match_threshold + 1:
		# print 'finding rule#0&1 with %s  existence', len(temp_results)
		hit_results.append(temp_results)

	return hit_results


def ruleCheckNeg(sentence, names, pattern):
	hit = pattern.search(sentence)

	# 如果句子过长，只判断命中位置前后60字符是否存在否定词或假设词
	if hit:
		temp_start = 0
		if hit.start() > 60:
			temp_start = hit.start() - 60
		# print 'sentence too long'
		temp_end = len(sentence)
		if hit.end() + 60 < len(sentence):
			temp_end = hit.end() + 60
		# print 'checking neg & uncertain in sentence:'
		# print sentence[temp_start: temp_end]
		if neg.search(sentence[temp_start: temp_end]) is None and uncertain.search(
				sentence[temp_start: temp_end]) is None:
			# print 'pattern exist without negative or uncertain words in this sentence:', sentence
			# print temp_start, "-", temp_end, ": ", sentence[temp_start:temp_end]
			# 如果不存在否定词或假设词，判断是否公司名字出现在命中位置前
			hit_result = existName(sentence, hit, names)
			if hit_result:
				hit_result["hitWord"] = sentence[hit.start():hit.end()]
				return hit_result
	return None


def existName(sentence, hit, names):
	# 如果句子过长，只判断命中位置前70字符是否公司名称
	if hit.start() > 70:
		sentence = sentence[hit.start() - 70: hit.start()]
	# print 'sentence too long'
	hit_name = names.search(sentence[: hit.start()])
	# print 'checking if the company names exist in the first half of the sentence'
	# print sentence[: hit.start()]
	if hit_name is not None:
		# print 'hit name: ', sentence[hit_name.start():hit_name.end()]
		return {"hitName:": sentence[hit_name.start():hit_name.end()]}
	# print 'FAILED FINDING COMPANY NAME'
	return None


def get_news_content(url, create_ts):
	"""
	根据公司名称获取新闻列表
	"""
	# import pdb
	# pdb.set_trace()
	news_bucket = S3.Bucket("search-key-news")
	try:
		obj = news_bucket.Object("text/%s/%s.text" % (create_ts, base64.b64encode(url)))
		content = obj.get()["Body"].read()
	except Exception as e:
		logger.error(e)
		return ""
	return content


@app.route("/api/results", methods=['POST'])
def post_results():
	paras = request.json
	initKeywords()
	name = paras.get('name')
	url = paras.get('id')
	print 'Current Rules:', len(rules)
	return json.dumps(checkContent(url, name))


if __name__ == "__main__":
	company_name = '重庆和友碱胺实业有限公司'
	r = requests.get('http://%s/api/news/strategy' % STRAT_IP, params={'name': company_name})
	strategies = r.json() if r.ok else {}
	print json.dumps(strategies, ensure_ascii=False, indent=2)
	create_ts = '2018-01-31 10:23:22'
	news_bucket = S3.Bucket("search-key-news")
	url = 'http://finance.qianlong.com/2018/0131/2366895.shtml'
	sc_id = 'c5f49e1f-8cbf-49fa-8d2a-106e81019b1d'
	res = {}
	try:
		create_ts = str(create_ts).split(' ')[0].replace('-', '/')
		obj = news_bucket.Object("text/%s/%s.text" % (create_ts, base64.b64encode(url)))
		content = obj.get()["Body"].read()
		strategies = new_strategy_types(strategies)
		temp = checkContent(url=sc_id, content=content.decode('utf-8'),
		                    strategies=strategies)
		if temp['hit']:
			res['hit_results'] = json.dumps(temp['hitResults'], ensure_ascii=False)
	except Exception as e:
		logger.error(e)
	print json.dumps(res, ensure_ascii=False)
