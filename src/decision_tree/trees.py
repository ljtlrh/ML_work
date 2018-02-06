#
from math import log
import operator
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

'''
输入：训练集 D={(x_1,y_1),(x_2,y_2),...,(x_m,y_m)};
      属性集 A={a_1,a_2,...,a_d}
过程：函数GenerateTree(D,A)
1: 生成节点node；
2: if D中样本全属于同一类别C then
3:    将node标记为C类叶节点，并返回
4: end if
5: if A为空 OR D中样本在A上取值相同 then
6:    将node标记为叶节点，其类别标记为D中样本数量最多的类，并返回
7: end if
8: 从A中选择最优划分属性 a*；    //每个属性包含若干取值，这里假设有v个取值
9: for a* 的每个值a*_v do
10:    为node生成一个分支，令D_v表示D中在a*上取值为a*_v的样本子集；
11:    if D_v 为空 then
12:       将分支节点标记为叶节点，其类别标记为D中样本最多的类，并返回
13:    else
14:       以GenerateTree(D_v,A\{a*})为分支节点
15:    end if
16: end for
'''
filepath = "../data/ljt_train_dx.txt"

def isNone(d):
    from operator import eq as cmp
    return (d is None or cmp(d, 'None') or
                    cmp(d, '?') or
                    cmp(d, '') or
                    cmp(d, 'NULL') or
                    cmp(d, 'null'))

def is_empty_data_delet(curLine):
    sum = 0.0
    if isinstance(curLine, list):
        for itrm in curLine:
            if isNone(itrm):
                itrm=0.0
            else:
                sum += float(itrm)
    if sum > 1:
        return False
    else:
        return True

def loadDataSet():
    dataMat = []
    labelMat = []
    fr = open(filepath)
    for line in fr.readlines():
        curLine = line.strip().split(',')
        if is_empty_data_delet(curLine):
            continue
        lineArr = []
        size = len(curLine)
        for i in range(size):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
    return dataMat


def dealdata(X, y):
    from sklearn.model_selection import train_test_split
    # 随机抽取20%的测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    return X_train, X_test, y_train, y_test

'''
    计算香农熵 -∑p(xi)log2p(xi)
'''
def calcShannonEnt(dataSet):
    '''
    信息熵是度量样本集合纯度最常用的一种指标，
    假设当前样本集合D中第k类样本所占的比例为prob，
    则D的信息熵定义为： Ent(D) = - sum(p_k*log(p_k, 2))
    :param dataSet:
    :return:
    '''
    numEntries = len(dataSet)
    lables = {}
    for featVec in dataSet:
        lable = featVec[-1]
        if lable not in lables.keys():
            lables[lable] = 0
        lables[lable] += 1
    shannonEnt = 0.0
    for key in lables:
        prob = float(lables[key])/numEntries
        shannonEnt -= prob*log(prob, 2)
    return shannonEnt




def creatDataSet():
    dataSet = [[1,1,'yes'],[1,1,'yes'],[1,0,'no'],[0,1,'no'],[0,1,'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels



'''
 划分数据集,找到某个特征和预期值相等的数据集
 dataSet:数据集
 axis:特征下标
 value:预期的值
'''
def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

'''
    选择最佳的划分方式
'''
def chooseBeatFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    # 计算信息熵，对平均不确定性的度量
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    print("bestFeature position:" +str(bestFeature))
    print("bestInfoGain values:" + str(bestInfoGain))
    return bestFeature, bestInfoGain

def majorityCnt(classList):
    '''
    如果数据集已经处理了所有特征属性，但类别标签依然不是唯一的，
    要定义叶子节点，多采用投票表决的方法决定该叶子节点的分类
    计算每个特征出现的频率：
    This function takes a list of class names and then creates a dictionary
whose keys are the unique values in  classList , and the object of the dictionary is the
frequency of occurrence of each class label from  classList . Finally, you use the
operator to sort the dictionary by the keys and return the class that occurs with the
greatest frequency.
    :param classList:
    :return:
    '''
    classCount={}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

labelsinfoList = []
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet] # 获取分类列表
    if classList.count(classList[0]) == len(classList):
        # 递归出口：1)如果是结果都是同一个标签直接返回，
        # 我们把当前节点标记为叶节点，并将其类别设定为该节点所含样本最多的类别；
        # 利用当前节点的后验分布
        return classList[0]
    if len(dataSet[0]) == 1:
        #2） 如果所有特征都使用完了，返回主要的标签，
        # 将其类别设定为其父节点所含样本最多的类别
        # 把父节点的样本分布作为当前节点的先验分布。
        return majorityCnt(classList)
    bestFeat,bestInfoGain = chooseBeatFeatureToSplit(dataSet)    # 找到决定性最高的特征下标
    bestFeatLabel = labels[bestFeat]
    print("bestFeatLabel==>>"+str(bestFeatLabel)+":"+"bestInfoGain:"+str(bestInfoGain))
    labelsinfoList.append({
        "bestFeatLabel":bestFeatLabel,
        "bestInfoGain":bestInfoGain
    })
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        print(myTree)
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    writejson("../data/ljt_train_feature_dx.josn", labelsinfoList)
    return myTree

def writejson(path, data):
    '''
     保存清洗数据
    '''
    import json
    # t1 = datetime.datetime.now()
    f = open(path, 'w')
    # 方式1，字典按keys顺序编码
    data_string = json.dumps(data, sort_keys=True, indent=2)

    # f.write(data_string.decode('unicode_escape'))
    f.write(data_string)
    f.write('\n')  # write不会在自动行末加换行符，�?要手动加�?
    f.flush()
    f.close()
'''
    绘图
'''
decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                    xytext=centerPt, textcoords='axes fraction', va='center',
                    ha='center', bbox=nodeType, arrowprops=arrow_args)

def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString)

def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = next(iter(myTree.keys()))
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0/ plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNode(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ =='dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(inTree,figpath):
    fig = plt.figure(111, facecolor='white')
    fig.clf()
    # createPlot.ax1 = plt.subplot(111, frameon=False)
    # plotNode('决策节点',(0.5, 0.1), (0.1, 0.5), decisionNode)
    # plotNode('叶子节点', (0.8, 0.1), (0.3, 0.8), leafNode)
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5/plotTree.totalW
    plotTree.yOff = 1.0
    plotTree(inTree, (0.5, 1.0), '')
    plt.savefig(figpath)
    plt.show()


def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = next(iter(myTree.keys()))
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = next(iter(myTree.keys()))
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth : maxDepth = thisDepth
    return maxDepth

def retrieveTree(i):
    listOfTrees = [{'no surfacing':{0:'no', 1:{'flippers':{0:'no',1:'yes'}}}},
                   {'no surfacing':{0:'no', 1:{'flippers':{0:{'head':{0:'no',1:'yes'}},1:'no'}}}}
                   ]
    return listOfTrees[i]

'''
    测试算法
'''
def classify(inputTree, featLabels, testVec):
    global classLabel
    firstStr = next(iter(inputTree.keys()))
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec);
            else:
                classLabel = secondDict[key]
    return classLabel

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


def Recall(P,TP):
    '''
    计算推荐结果的召回率,原本为对的当中预测为对的比例
    :param P: POSITIVE 正样本
    :param TP: TRUE POSITIVE 真正，被模型预测为正测正样本
    :return:
    '''

    return TP / (P * 1.0)


def Precision(TP, FP):
    '''
    计算推荐结果的准确率，预测为对当中原本为对的的比例
    :param TP: TRUE POSITIVE 真正，被模型预测为正的正样本
    :param FP: False POSITIVE 假正，被模型预测为正样本的负样本
    :return:
    '''
    return TP / (TP*1.0 + FP*1.0)

def TP_RATE(P, TP):
    '''
    正确率：原本是对的预测为对的比率
    :param P:  正样本
    :param TP: 真正，被模型预测为正的正样本
    :return:
    '''
    return TP / (P*1.0)

def FP_RATE(N, FP):
    '''
    错误率：原本是错的预测为对的比率
    :param N:  负样本
    :param FP: 假正，被模型预测为正的负样本
    :return:
    '''
    return FP / (N*1.0)

def ROC_AUC(y, pred):
    from sklearn.metrics import roc_curve, auc
    # y = np.array([1, 1, 2, 2])
    # pred = np.array([0.1, 0.4, 0.35, 0.8])
    fpr, tpr, thresholds = roc_curve(y, pred, pos_label=2)
    print("正确率：fpr==>"+str(fpr))
    print("错误率：tpr==>"+str(tpr))
    print(thresholds)
    from sklearn.metrics import auc
    auc_area = auc(fpr, tpr)
    # 画图，只需要plt.plot(fpr,tpr),变量roc_auc只是记录auc的值，通过auc()函数能计算出来
    plt.plot(fpr, tpr, lw=1, label='ROC  (area = %0.2f)' % ( auc_area))
    print(auc_area)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

def glasess():
    '''
    隐形眼镜
    :return:
    '''
    fr = open('lenses.txt')
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels=['age','prescript', 'astigamtic', 'tearRate']
    myTree= createTree(lenses, lensesLabels)
    print(labelsinfoList)
    print(myTree)
    # 存储分类器
    storeTree(myTree,"glasess_tree01.txt")
    tree01= grabTree("glasess_tree01.txt")
    createPlot(tree01, figpath="glasess.png")
    lensesLabels = ['age','prescript', 'astigamtic', 'tearRate']
    pre01 = classify(tree01,lensesLabels, ["pre","hyper","no","normal"])
    print(pre01)



def dx_classfy():
    '''
       吊销
    '''
    # 1）加载数据
    train_data_dx = loadDataSet()
    # 2）随机划分训练集和测试集
    X_train, X_test = train_test_split(train_data_dx,  test_size=0.3, random_state=0)
    dxFeature = ["judgedoc_is_no", "judgedoc_cnt", "litigant_defendant_cnt", "near_3_year_judgedoc_cnt",
                 "near_2_year_judgedoc_cnt", "near_1_year_judgedoc_cnt", "litigant_defendant_contract_dispute_cnt",
                 "litigant_defendant_bust_cnt", "litigant_defendant_infringe_cnt",
                 "litigant_defendant_Intellectual_property_owner_cnt", "litigant_defendant_unjust_enrich_cnt",
                 "litigant_result_sum_money", "net_judgedoc_defendant_cnt",
                 "shixin_is_no", "shixin_cnt", "near_3_year_shixin_cnt", "near_2_year_shixin_cnt",
                 "near_1_year_shixin_cnt", "court_announce_is_no",
                 "court_announce_cnt", "court_announce_litigant_cnt", "court_notice_is_no", "court_notice_cnt",
                 "court_notice_litigant_cnt"]
    # 3）训练决策树模型
    tree = createTree(X_train, dxFeature)
    # 存储分类器
    storeTree(tree, "dx_tree01.txt")
    # 4) 持久化中间数据
    writejson("../data/ljt_train_tree_dx.josn", tree)
    # 5）画图
    createPlot(tree, "dx_tree01.png")
    # 6） 测试
    dxFeature01 = ["judgedoc_is_no", "judgedoc_cnt", "litigant_defendant_cnt", "near_3_year_judgedoc_cnt",
                 "near_2_year_judgedoc_cnt", "near_1_year_judgedoc_cnt", "litigant_defendant_contract_dispute_cnt",
                 "litigant_defendant_bust_cnt", "litigant_defendant_infringe_cnt",
                 "litigant_defendant_Intellectual_property_owner_cnt", "litigant_defendant_unjust_enrich_cnt",
                 "litigant_result_sum_money", "net_judgedoc_defendant_cnt",
                 "shixin_is_no", "shixin_cnt", "near_3_year_shixin_cnt", "near_2_year_shixin_cnt",
                 "near_1_year_shixin_cnt", "court_announce_is_no",
                 "court_announce_cnt", "court_announce_litigant_cnt", "court_notice_is_no", "court_notice_cnt",
                 "court_notice_litigant_cnt"]
    TP = 0
    FP = 0
    TN = 0
    FN = 0
    P = 0
    N = 0
    pre_result = []
    TrueResult = []
    for itemTVect in X_test:
        textVect = itemTVect[:24]
        y = itemTVect[-1]
        TrueResult.append(y)
        if y == 0:
            # 正样本
            P += 1
        else:
            N += 1
        pre01 = classify(tree, dxFeature01, textVect)
        if pre01 == y and pre01 == 0: # TP，真正
            TP += 1
        elif pre01 == y and pre01 == 0: # TN，真负
            TN += 1
        elif pre01 != y and pre01 == 1: # FN， 假负
            FN += 1
        elif pre01 != y and pre01 == 0: # FP， 假正
            FP += 1
        pre_result.append(pre01)
    recall = Recall(P, TP)
    print("召回率："+str(recall))
    precision = Precision(TP, FN)
    print("准确率："+str(precision))
    print("调和平均数：" + str(2.0/((1.0/precision)+(1.0/recall))))
    ROC_AUC(y=TrueResult,pred=pre_result)



if __name__ == "__main__":
    import time
    start = time.time()
    # data, label = creatDataSet()
    # data, label = loadDataSet()
    # tree = createTree(data, label)

    # myTree = retrieveTree(0)
    # myTree['no surfacing'][3]='maybe'
    # createPlot(tree)
    # data, label = creatDataSet()
    # print(classify(tree, label,[1,1]))
    glasess()
    # dx_classfy()
    print('Cost time: %f' % (time.time() - start))