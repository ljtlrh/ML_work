# -*- coding: utf-8 -*-
import json
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier


class DecisionTreeClassifierParser(object):
	'''
	对决策树进行解析
	'''

	def __init__(self, model, feature_names):
		'''
		:param model: 已训练完成的决策树模型
		:param feature_names: list类型，训练数据的特征名字，按训练时的顺序排列
		:return:
		'''
		self.model = model
		self.feature_names = feature_names
		# 仅支持DecisionTreeClassifier模型
		if not isinstance(self.model, DecisionTreeClassifier):
			raise ('The given model is not the supported sklearn model DecisionTreeClassifier')

	def __parser(self):
		'''
		递归算法解析决策树的每个分支
		参考部分代码：　https://stackoverflow.com/questions/20224526/how-to-extract-the-decision-rules-from-scikit-learn-decision-tree
		:return:
		'''
		parsed_tree = []
		# 左节点id
		left = self.model.tree_.children_left
		# 右节点id
		right = self.model.tree_.children_right
		# 节点阈值
		threshold = self.model.tree_.threshold
		# 特征名字
		features = [self.feature_names[i] for i in self.model.tree_.feature]
		# value 是该节点上不同标签样本的数量
		values = self.model.tree_.value
		# 该节点sample的总数量，理论上value的和即为sample的总数
		number_of_nodes = self.model.tree_.weighted_n_node_samples
		# 节点不纯度
		# impurity = tree.tree_.impurity
		# 叶子节点id列表
		idx = np.argwhere(left == -1)[:, 0]

		def recurse(left, right, child, lineage=None):
			if lineage is None:
				v = values[child][0]
				label = np.argmax(v)
				# 该节点误分率
				missclassfication_rate = min(v) / sum(v)
				# node_impurity = impurity[child]
				# 终节点id, 标签，训练集中归于该节点的数量，错分概率
				lineage = [(child, 'leaf', label, int(number_of_nodes[child]), missclassfication_rate)]
			if child in left:
				parent = np.where(left == child)[0].item()
				split = '<='
			else:
				parent = np.where(right == child)[0].item()
				split = '>'

			lineage.append((parent, split, threshold[parent], features[parent]))

			if parent == 0:
				lineage.reverse()
				return lineage
			else:
				return recurse(left, right, parent, lineage)

		for child in idx:
			one_branch = []
			for node in recurse(left, right, child):
				one_branch.append(node)
			parsed_tree.append(one_branch)
		return parsed_tree

	def get_parsed_tree(self):
		'''输出决策树的解析结果.
		Returns
		-------
		[
		  {
			"missclassfication_rate": 0.5, #改路径错误分类率
			"sample_number": 2,　#该路径样本数据量
			"statement": "col2 <= 5.5 and col1 <= 1.5 and col2 <= 3.5",　#该路径的条件组合, 并且作冗余的归并，例如col2 > 3.5 and col2 > 4.5归并为col2 > 4.5
			"label": 0　#该路径的样本被预测的标签
		  }
		]
		'''
		res = []
		for t in self.__parser():
			sub_statement = []
			sub_statement_container = {}  # 以col1 <=作为key
			for each in t[0:-1]:
				# 可互相包含的决策路径逻辑合并处理
				statement_key = str(each[3]) + ' ' + str(each[1])
				if statement_key in sub_statement_container.keys():
					if each[1] == '>' and sub_statement_container[statement_key] < each[2]:
						sub_statement.remove(statement_key + ' ' + str(sub_statement_container[statement_key]))
						sub_statement.append(statement_key + ' ' + str(each[2]))
						sub_statement_container[statement_key] = each[2]
					elif each[1] == '<=' and sub_statement_container[statement_key] > each[2]:
						sub_statement.remove(statement_key + ' ' + str(sub_statement_container[statement_key]))
						sub_statement.append(statement_key + ' ' + str(each[2]))
						sub_statement_container[statement_key] = each[2]
				else:
					sub_statement_container[statement_key] = each[2]
					sub_statement.append(str(each[3]) + ' ' + str(each[1]) + ' ' + str(each[2]))
			res.append({
				'decision_path': ' and '.join(sub_statement),  # 以and的形式组合
				'label': t[-1][2],
				'sample_number': t[-1][3],
				'missclassfication_rate': t[-1][4]
			})

		return res


if __name__ == "__main__":
	from sklearn.datasets import load_iris
	from sklearn.model_selection import train_test_split

	iris = load_iris()
	X = iris.data
	y = iris.target
	names = iris.feature_names
	X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)

	dt = DecisionTreeClassifier()
	dt.fit(X_train, y_train)
	dtp = DecisionTreeClassifierParser(dt, names)
	res = dtp.get_parsed_tree()
	print json.dumps(res, ensure_ascii=False, indent=2)

	print '另一个例子'
	print '*' * 100
	# dummy data:
	df = pd.DataFrame({'col1': [0, 1, 2, 3], 'col2': [3, 4, 5, 6], 'label': [0, 1, 0, 1]})
	# create decision tree
	dt = DecisionTreeClassifier(max_depth=5, min_samples_leaf=1)
	dt.fit(df.ix[:, :2], df.label)
	names = df.columns
	dtp = DecisionTreeClassifierParser(dt, names)
	res = dtp.get_parsed_tree()
	print json.dumps(res, ensure_ascii=False, indent=2)
