#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 1329331182@qq.com
@site: 
@software: PyCharm
@file: factory_demo.py
@time: 18-4-25 上午11:35
"""


class Fruit(object):
    def __init__(self):
        pass

    def print_color(self):
        pass


class Apple(Fruit):
    def __init__(self):
        pass

    def print_color(self):
        print("Apple is red")


class Orange(Fruit):
    def __init__(self):
        pass

    def print_color(self):
        print("Orange is orange")


class FruitFactory(object):
    fruits = {"apple": Apple, "orange": Orange}

    def __new__(cls, name):
        if name in cls.fruits.keys():
            return cls.fruits[name]()
        else:
            return Fruit()


fruit01 = FruitFactory('apple')
fruit02 = FruitFactory('orange')
fruit01.print_color()
fruit02.print_color()