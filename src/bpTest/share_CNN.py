from __future__ import division
from __future__ import print_function
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import tensorflow as tf



def loadData(fileName):
    numFeat = len(open(fileName).readline().strip().split('\t')) - 1
    dataMat = []
    labelMat = []
    fr = open(fileName)
    for line in fr.readlines():
        lineArr = []
        curLine = line.strip().split('\t')
        if curLine[0] == '800':
            continue
        for i in range(numFeat):
            lineArr.append(float(curLine[i]))
        dataMat.append(lineArr)
        labelMat.append(float(curLine[-1]))
    return dataMat, labelMat

# df_sh = ts.get_sz50s()['code']
df_sh = ["600016"]
fac = []
ret = []
facT = []
retT = []
predFAC = []
learning_rate = 0.001
batch_size = 10
print(int(fac.shape[0]))
training_iters = int(fac.shape[0] / batch_size)
display_step = 10

# Network Parameters
n_input = 14
n_steps = 10
n_hidden = 1024
n_classes = 3
dropout = 0.8
# tf Graph input
xArr, yArr = loadData('data.txt')
# 取最近的160数据
fac = xArr[0:159][:]
ret = yArr[0:159]
x = tf.placeholder('float', [None, n_steps, n_input])
y = tf.placeholder('float', [None, n_classes])
keep_prob = tf.placeholder(tf.float32)  # dropout (keep probability)


def CNN_Net_five(x, weights, biases, dropout=0.8, m=1):
    x = tf.reshape(x, shape=[-1, 10, 14, 1])

    # 卷积层1
    x = tf.nn.conv2d(x, weights['wc1'], strides=[1, m, m, 1], padding='SAME')
    x = tf.nn.bias_add(x, biases['bc1'])
    x = tf.nn.relu(x)

    # 卷积层2
    x = tf.nn.conv2d(x, weights['wc2'], strides=[1, m, m, 1], padding='SAME')
    x = tf.nn.bias_add(x, biases['bc2'])
    x = tf.nn.relu(x)

    # 卷积层3
    x = tf.nn.conv2d(x, weights['wc3'], strides=[1, m, m, 1], padding='SAME')
    x = tf.nn.bias_add(x, biases['bc3'])
    x = tf.nn.relu(x)

    # 卷积层4
    x = tf.nn.conv2d(x, weights['wc4'], strides=[1, m, m, 1], padding='SAME')
    x = tf.nn.bias_add(x, biases['bc4'])
    x = tf.nn.relu(x)

    # 卷积层5
    x = tf.nn.conv2d(x, weights['wc5'], strides=[1, m, m, 1], padding='SAME')
    x = tf.nn.bias_add(x, biases['bc5'])
    x = tf.nn.relu(x)

    # 全连接层
    x = tf.reshape(x, [-1, weights['wd1'].get_shape().as_list()[0]])
    x = tf.add(tf.matmul(x, weights['wd1']), biases['bd1'])
    x = tf.nn.relu(x)

    # Apply Dropout
    x = tf.nn.dropout(x, dropout)
    # Output, class prediction
    x = tf.add(tf.matmul(x, weights['out']), biases['out'])
    return x


# Store layers weight & bias
weights = {
    'wc1': tf.Variable(tf.random_normal([5, 5, 1, 16])),
    'wc2': tf.Variable(tf.random_normal([5, 5, 16, 32])),
    'wc3': tf.Variable(tf.random_normal([5, 5, 32, 64])),
    'wc4': tf.Variable(tf.random_normal([5, 5, 64, 32])),
    'wc5': tf.Variable(tf.random_normal([5, 5, 32, 16])),
    # fully connected, 7*7*64 inputs, 1024 outputs
    'wd1': tf.Variable(tf.random_normal([n_steps * n_input * 16, 1024])),
    'out': tf.Variable(tf.random_normal([1024, n_classes]))
}

biases = {
    'bc1': tf.Variable(tf.random_normal([16])),
    'bc2': tf.Variable(tf.random_normal([32])),
    'bc3': tf.Variable(tf.random_normal([64])),
    'bc4': tf.Variable(tf.random_normal([32])),
    'bc5': tf.Variable(tf.random_normal([16])),
    'bd1': tf.Variable(tf.random_normal([1024])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

pred = CNN_Net_five(x, weights, biases, dropout=keep_prob)
cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(pred, y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
correct_pred = tf.equal(tf.argmax(pred, 1), tf.arg_max(y, 1))
# tf.argmax(input,axis=None) 由于标签的数据格式是 -1 0 1 3列，该语句是表示返回值最大也就是1的索引，两个索引相同则是预测正确。
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
# 更改数据格式，降低均值
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    print("**")
    print(training_iters)
    for tr in range(15):
        # for tr in range(3):
        for i in range(int(len(fac) / batch_size)):
            batch_x = fac[i * batch_size:(i + 1) * batch_size].reshape([batch_size, n_steps, n_input])
            batch_y = ret[i * batch_size:(i + 1) * batch_size].reshape([batch_size, n_classes])
            sess.run(optimizer, feed_dict={x: batch_x, y: batch_y, keep_prob: dropout})
            if (i % 50 == 0):
                print(i, '----', (int(len(fac) / batch_size)))
        loss, acc = sess.run([cost, accuracy], feed_dict={x: batch_x, y: batch_y, keep_prob: 0.8})
        print("Iter " + str(tr * batch_size) + ", Minibatch Loss= " + "{:.26f}".format(
            loss) + ", Training Accuracy= " + "{:.26f}".format(acc))
    print("Optimization Finished!")
    print("Accuracy in data set")
    test_data = fac[:batch_size].reshape([batch_size, n_steps, n_input])
    test_label = ret[:batch_size].reshape([batch_size, n_classes])
    loss, acc = sess.run([cost, accuracy], feed_dict={x: test_data, y: test_label, keep_prob: 1.})
    print("Accuracy= " + "{:.26f}".format(acc))

    print("Accuracy out of data set")
    test_dataT = facT[:len(facT)].reshape([len(facT), n_steps, n_input])
    test_labelT = retT[:len(facT)].reshape([len(facT), n_classes])
    loss, acc = sess.run([cost, accuracy], feed_dict={x: test_dataT, y: test_labelT, keep_prob: 1.})
    print("Accuracy= " + "{:.26f}".format(acc))

    pred_dataT = predFAC[:batch_size].reshape([1, n_steps, n_input])
    pred_lable = sess.run([pred], feed_dict={x: pred_dataT, keep_prob: 1.})
    list_lable = pred_lable[0][0]
    maxindex = np.argmax(list_lable)
    # print("Predict_label is " + str(pred_lable[0][0]))
    if (maxindex == 0):
        print("up")
    else:
        print("down")
    sess.close()