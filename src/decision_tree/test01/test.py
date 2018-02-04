import operator
import sys
# sys.path.append('C:\Users\ljt\PycharmProjects\ML_work\src\decision_tree\test01\Trees.py');
# sys.path.append('C:\Users\ljt\PycharmProjects\ML_work\src\decision_tree\test01\treePlotter.py');
import src.decision_tree.test01.Trees as Trees
import src.decision_tree.test01.treePlotter

#fr = open('E:\machinelearninginaction\Ch03\lenses.txt');
#lenses = [inst.strip().split('\t') for  inst in fr.readlines()]
#lensesLabels = ['age','prescript','astigmatic','tearRate']
#lensesTree = Trees.createTree(lenses,lensesLabels)
#print(lensesTree)
#treePlotter.createPlot(lensesTree);

dataSet,labels = Trees.createDataSet()
print(labels)

mytree = Trees.createtree(dataSet,labels)
Trees.storeTree(mytree,"testTree01.txt")
mytree01 = Trees.grabTree("testTree01.txt")
label = Trees.classify(mytree01, labels, [1, 0])

print(label)
