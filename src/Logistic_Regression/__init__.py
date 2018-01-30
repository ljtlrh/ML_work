'''
    逻辑回归
    回归算法的核心就是找到一条线（二维），使得大部分个体的所有特征参数落在这条线上，所要做的就是使这个误差最小，之后一个新的个体，通过这条线的表达式就能够计算出来。
    所以问题的关键就在于误差最小，一般使用梯度下降算法。回归算法也被视为最优化算法
    逻辑回归使用了一个特殊的函数Sigmoid函数，使得所有结果只会落在两个位置，这样就是一种分类算法了
    优点：计算代价不高，易于理解和实现
    缺点：容易欠拟合，分类精度可能不高
    使用数据类型：数值型和标称型数据
'''