from math import *
import operator


'''
    存储决策树
'''
def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'wb')
    pickle.dump(inputTree, fw)
    fw.close()

def grabTree(filename):
    '''
     加载存储在磁盘上的 决策树
    :param filename:
    :return:
    '''
    import pickle
    fr = open(filename, 'rb')
    return pickle.load(fr)

def createDataSet():
    dataSet = [[1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no'],
               [1,1,'yes']];

    labels = ['no surfacing','flippers'];
    return  dataSet,labels

'''计算集合的信息熵'''
def calcShannonEnt(dataSet):
    numEntries = len(dataSet) #获得输入集合的条数
    labelCounts={}#存放标签的字典
    # for i in range(numEntries): 标准C语言的思维啊
    #     lable = dataSet[i][-1]
    for featVec in dataSet:#遍历集合
        label = featVec[-1]
        if label not in labelCounts.keys():
            labelCounts[label] = 0;
        labelCounts[label] += 1;
    shannonEnt = 0.0
    for key in labelCounts:#计算香农熵
        prob = float(labelCounts[key])/numEntries #计算比例
        shannonEnt -= prob*log(prob,2)
    return shannonEnt


'''根据给定的数据标签和值来划分数据集'''
def splitDataSet(dataSet,axis,value):
    retDataSet = []
    for featVect in dataSet:
        if featVect[axis] == value:
            reducedFeatVect = featVect[:axis] #添加数据0--axis
            reducedFeatVect.extend(featVect[axis+1:])#添加数据axis--end
            retDataSet.append(reducedFeatVect)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])-1;
    baseEntropy = calcShannonEnt(dataSet) #计算划分前的信息熵
    bastInfoGain = 0.0;
    bestFeature = -1;
    datasetSize = len(dataSet)
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet ] #获得特征列表集合
        uniqueVals = set(featList)#属性去重
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet,i,value) #根据属性划分自己，我误将每行理解成了一个划分后的子集，思维不完备
            prob = float(len(subDataSet) )/ datasetSize; #计算概率
            newEntropy += prob*calcShannonEnt(subDataSet) #计算每个子集的信息熵与概率的乘积

        infoGain = baseEntropy - newEntropy;
        if ( infoGain > bastInfoGain ): #选择最大的信息熵
            bastInfoGain =  infoGain;
            bestFeature = i;

    return bestFeature;

'''计算信息增益时，采用公式infoGain = baseEntropy - newEntropy计算信息增益，然后取最大值
    上述计算公式等价于求最小的newEntropy
'''
def chooseBestFeatureToSplitAsMyWay(dataset):
    numFeatures = len(dataset[0])-1
    bestFeature = -1;
    minEntropy = 0.0;
    dataSetSize = len(dataset)
    for i in range(numFeatures):
        featuresList = [vec[i] for vec in dataset];
        uniqFeature = set(featuresList)
        newEntropy = 0.0;
        for value in uniqFeature:
            subDataSet = splitDataSet(dataset,i,value);
            prob = float(len(subDataSet))/dataSetSize;
            newEntropy += prob*calcShannonEnt(subDataSet);

        if(minEntropy > newEntropy or bestFeature==-1):
            minEntropy = newEntropy;
            bestFeature = i;
    return bestFeature

'''如果已经处理了所有属性，但是类标签任不唯一，采用多数表决的方法加以处理'''
def majorityLabel(labelList):
    labelCount = {};
    for label in labelList:
        if label not in labelCount:
            labelCount[label] = 0;
        labelCount[label] += 1;
    sortedCount = sorted(labelCount.items(),key=operator.itemgetter(1),reversed=True);
    return  sortedCount[0][0]

"""
    采用递归的方式创建树
"""
def createtree(dataset,labels):
    classList = [vect[-1] for vect in dataset] #获得数据集中的所有的类别
    if classList.count(classList[0])  == len(classList):# 如果所有的数据都有相同的分类，则直接返回这个分类
        return classList[0]
    if len(dataset[0]) ==1 :#程序遍历完所有的属性，此时只剩下标签，则采用多数表决法决定标签
        return majorityLabel(classList)
    labelscp = labels[:]
    bestFeature = chooseBestFeatureToSplitAsMyWay(dataset); #选择最佳属性进行分裂
    bestLabel = labelscp[bestFeature];#最佳属性的名称
    del(labelscp[bestFeature])#从属性列表中删除最佳属性
    mytree = {bestLabel:{}}#利用字典类型来存储树的信息  {'bufu': {0: 1, 1: 1, 2: 1, 3: 1}}
    featValues = [vect[bestFeature] for vect in dataset] #获得最佳属性的所有值
    uniqFeatValue = set(featValues)#最佳属性所有值去重

    for value in uniqFeatValue:
        sublabels = labelscp[:]
        mytree[bestLabel][value] = createtree(splitDataSet(dataset,bestFeature,value),sublabels) #递归创建子树
    return mytree

'''分类识别函数'''
def classify(inputTree,labels,testVect):
    firstStr = list(inputTree.keys())[0]
    # firstStr = inputTree.keys()[0];#获得当前树的根属性的key值
    secondDict = inputTree[firstStr];#获得根节点的子树集合
    feataindex = labels.index(firstStr);#获得当前根属性标签在属性集合中的位置

    for key in secondDict.keys():#遍历当前属性的对应的所有值
        if testVect[feataindex] == key:
            # if type(secondDict[key])._name_=='dict' :#属性对应的值是一个字子树，递归处理
            if isinstance(secondDict[key],(dict)):
                classlabel = classify(secondDict[key],labels,testVect);
            else: classlabel = secondDict[key]#直接返回标签

    return  classlabel