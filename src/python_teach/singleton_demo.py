#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 1329331182@qq.com
@site: __init__ 初始化对象 和 __new__  实例化对象,Python中的构造方法
@software: PyCharm
@file: singleton_demo.py
@time: 18-4-25 上午10:08
"""


class Person(object):
    def __init__(self, name, age):
        print("init")
        self.name = name
        self.age = age


p = Person("lll", 25)
print(p)
p1 = Person("lll", 25)
print(p1)


# __new__()是静态方法,__init__()是实例方法

class Person02(object):
    def __new__(cls, *args, **kwargs):
        print("new instance")
        instance = object.__new__(cls, *args, **kwargs)
        return instance

    def __init__(self, name, age):
        print("init")
        self.name = name
        self.age = age


p = Person02("lll", 25)
p1 = Person02("lll", 26)
print(p)
print(p.age)
print(p1)
print(p1.age)


# 单例模式
class Person03(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        print("new instance")
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, name, age):
        print("init")
        self.name = name
        self.age = age


p = Person03("lll", 25)
p1 = Person03("lll", 26)
print(p)
print(p.age)
print(p1)
print(p1.age)
# 通过对__new__()方法实例的创建的控制可以实现每次声明都指向同一个地址