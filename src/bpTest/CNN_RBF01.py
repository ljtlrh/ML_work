# coding=utf8
'''
Created on 2018��1��25��

@author:  
'''

import xlrd
import tensorflow as tf
import numpy as np
import pandas as pd
 

def loadData(book01,book02):
    '''
         初始化数据
    '''
    dx = pd.read_excel(book01, sheetname='Sheet1')
    dY = pd.read_excel(book02, sheetname='Sheet1')
    dataMat = dx
    labelMat = dY
    print(dx.__len__())
    print(dx.__len__())
    pd.Series(dx,dY)
    print(dataMat)
    print(labelMat)
    return dataMat, labelMat

def CNN_Net_five(x, weights, biases, dropout=0.8, m=1):
    x = tf.reshape(x, shape=[-1, 10, 14, 1])

    # �����1
    x = tf.nn.conv2d(x, weights['wc1'], strides=[1, m, m, 1], padding='SAME')
    x = tf.nn.bias_add(x, biases['bc1'])
    x = tf.nn.relu(x)

    # �����2
    x = tf.nn.conv2d(x, weights['wc2'], strides=[1, m, m, 1], padding='SAME')
    x = tf.nn.bias_add(x, biases['bc2'])
    x = tf.nn.relu(x)

    # �����3
    x = tf.nn.conv2d(x, weights['wc3'], strides=[1, m, m, 1], padding='SAME')
    x = tf.nn.bias_add(x, biases['bc3'])
    x = tf.nn.relu(x)

    # �����4
    x = tf.nn.conv2d(x, weights['wc4'], strides=[1, m, m, 1], padding='SAME')
    x = tf.nn.bias_add(x, biases['bc4'])
    x = tf.nn.relu(x)

    # �����5
    x = tf.nn.conv2d(x, weights['wc5'], strides=[1, m, m, 1], padding='SAME')
    x = tf.nn.bias_add(x, biases['bc5'])
    x = tf.nn.relu(x)

    # ȫ���Ӳ�
    x = tf.reshape(x, [-1, weights['wd1'].get_shape().as_list()[0]])
    x = tf.add(tf.matmul(x, weights['wd1']), biases['bd1'])
    x = tf.nn.relu(x)

    # Apply Dropout
    x = tf.nn.dropout(x, dropout)
    # Output, class prediction
    x = tf.add(tf.matmul(x, weights['out']), biases['out'])
    return x
 

if __name__ == '__main__':
    keep_prob = tf.placeholder(tf.float32)  # dropout (keep probability)
    learning_rate = 0.001
    batch_size = 10
    print(int(fac.shape[0]))
    training_iters = int(fac.shape[0] / batch_size)
    display_step = 10
    # Network Parameters
    n_input = 14
    n_steps = 10
    n_hidden = 1024
    dropout = 0.8
    # tf Graph input
    x = tf.placeholder('float', [None, n_steps, 1701])
    y = tf.placeholder('float', [None, None])
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
    # tf.argmax(input,axis=None) ���ڱ�ǩ�����ݸ�ʽ�� -1 0 1 3�У�������Ǳ�ʾ����ֵ���Ҳ����1������������������ͬ����Ԥ����ȷ��
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    # �������ݸ�ʽ�����;�ֵ
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        sess.close() 
    R = 0.0
    pred = CNN_Net_five(x)
    x_test=xs3
    y_test=xs4
    error_cnn=abs(pred-y_test)/y_test
    predsum = ((n*sum(pred^2)-sum(pred)^2)*(n*sum(y_test^2)-sum(y_test)^2))
    testpre = (n*sum(pred*y_test)-sum(pred))^2
    R = (testpre / predsum) ^ 2
    print(R)
