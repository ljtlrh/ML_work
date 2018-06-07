# -*- coding: utf-8 -*-
# __author__ = 'Yuanjiang Huang'
# yuanjiang.huang@socialcredits.cn

import os
import json
import re

from scpy.logger import get_logger

from data.caseReasonCode import CASE_CODE_LIST, EXTRA_CASE_REASON_MAPPING

logger = get_logger(__file__)
CURRENT_PATH = os.path.dirname(__file__)
if CURRENT_PATH:
	CURRENT_PATH = CURRENT_PATH + '/'

# 缺省的案由
DEFAULT_CASE_TYPE = u"其他"

#最终输出的案由列表
MAPPED_CASE = [
	u"刑事案由",
	u"人格权纠纷",
	u"婚姻家庭、继承纠纷",
	u"物权纠纷",
	u"合同纠纷",
	u"不当得利纠纷",
	u"无因管理纠纷",
	u"知识产权合同纠纷",
	u"知识产权权属、侵权纠纷",
	u"不正当竞争纠纷",
	u"垄断纠纷",
	u"劳动争议",
	u"人事争议",
	u"海事海商纠纷",
	u"与企业有关的纠纷",
	u"与公司有关的纠纷",
	u"合作企业纠纷",
	u"与破产有关的纠纷",
	u"证券纠纷",
	u"期货交易纠纷",
	u"信托纠纷",
	u"保险纠纷",
	u"票据纠纷",
	u"信用证纠纷",
	u"侵权责任纠纷",
	u"适用特殊程序案件案由",
	u"行政案由",
	u"赔偿案由",
]


def find_mapping_case_reason_code():
	res = {}
	for name in MAPPED_CASE:
		for r in CASE_CODE_LIST:
			reason = r.get('name').decode('utf-8')
			if reason == name:
				res[name] = r.get('id')
	return res


# 预加载案由到代码的映射关系
CASE_REASON_CODE = find_mapping_case_reason_code()

class caseReasonMapping(object):
	def __init__(self, case):
		self.case = case
		if not isinstance(self.case, unicode):
			raise TypeError('The provided case reason code should be unicode type, %s type found.' % str(type(case)))
		self.case_reason_code = CASE_REASON_CODE

	# logger.info('Load the code for cases done.')

	def find_mapping_type_from_extra_dict(self, case):
		'''
		从固定映射列表中找案由映射关系
		:param case:
		:return:
		'''
		return EXTRA_CASE_REASON_MAPPING.get(case, None)

	def start_with(self, data, start):
		'''
		以data是否以start开头
		:param data:
		:param start:
		:return:
		'''
		if not isinstance(start, str) or not isinstance(data, str):
			raise TypeError('The input for the regex matching should be a string')
		pattern = '^' + start
		if re.findall(pattern=pattern, string=data):
			return True
		else:
			return False

	def find_code_for_a_case(self, case):
		'''
		在CASE_CODE_LIST中找case对应的id, 找不到就返None
		:param case:
		:return:
		'''
		for item in CASE_CODE_LIST:
			if case == item.get('name').decode('utf-8'):
				return item.get('id')
		return None

	def get_mapped_case_reason(self):
		'''
		找case映射以后的案由, 结果为一列表，因为一个案由可能对应多个
		如果映射不出，则返“其他”
		:param case:
		:return:
		'''
		results = []

		# 如果输入案由为映射结果本身
		if self.case in MAPPED_CASE:
			results.append(self.case)
			return results

		# 如果从固定的映射表找到映射关系
		mapping = self.find_mapping_type_from_extra_dict(self.case)

		if mapping:
			results.append(mapping)
			return results
		#否则，找出案由对应的code (或者id)
		code = self.find_code_for_a_case(self.case)
		if code:
			for k, v in self.case_reason_code.iteritems():
				# 　找code对应子类或者父类
				if self.start_with(code, v) or self.start_with(v, code):
					results.append(k)
			if not results:
				results.append(DEFAULT_CASE_TYPE)
				return results
		else:
			results.append(DEFAULT_CASE_TYPE)
			return results
		return results


if __name__ == "__main__":
	# start_with('002312112','0123')
	case = u'加工合同纠纷'
	# case = u"交通运输行政管理(交通)-航空行政管理(航空)"
	case = u"工程重大安全事故"
	case = u"储蓄存款合同纠纷"
	case = u"农村建房施工合同纠纷"
	case = u"侵害商标权纠纷"
	# case = u"合同、无因管理、不当得利纠纷"
	# case = u"民事案由"
	# case = u"不存在的案由"
	c = caseReasonMapping(case=case)
	print json.dumps(c.get_mapped_case_reason(), ensure_ascii=False, indent=2)
