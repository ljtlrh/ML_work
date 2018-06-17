#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 2018/5/2 14:39
# @Author  : liujiantao
# @Site    : 
# @File    : graph_session_tensor.py
# @Software: PyCharm
import tensorflow as tf
g1 = tf.Graph()
with g1.as_default():
    # 在计算图g1中定义变量‘v’,并初始化为0
    v = tf.get_variable('v', [1], initializer=tf.zeros_initializer())
g2 = tf.Graph()
with g2.as_default():
    v = tf.get_variable("v", [1], initializer = tf.ones_initializer())  # 设置初始值为1
#在计算图g1中读取变量‘V’的值
with tf.Session(graph=g1) as sess:
    tf.global_variables_initializer().run()
    with tf.variable_scope("",reuse=True):
        # 在计算图g1中，变量“v”的取值应该为0
        print(sess.run(tf.get_variable("v")))
with tf.Session(graph = g2) as sess:
    tf.global_variables_initializer().run()
    with tf.variable_scope("", reuse=True):
        print(sess.run(tf.get_variable("v")))