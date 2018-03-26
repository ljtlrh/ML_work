#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 2018/3/22 21:37
# @Author  : liujiantao
# @Site    : 
# @File    : map_reduce_filter_fun.py
# @Software: PyCharm
def create_tuple(args, length):
    ''' Creates a tuple of elements of a list at the index length '''
    if not args:
        return ()
    else:
        try:
            return (args[0][length],) + create_tuple(args[1:], length)
        except(IndexError):
            return (None,) + create_tuple(args[1:], length)

def create_list(args, length):
    ''' creates a list of tuples from the tuple of lists in such manner that
    the first element of each list is made as a tupple
    sample:
        input - ([1, 2, 4, 5, 6], [4, 5, 6])
        output - [(1, 2), (2, 5), (4, 6), (5, None), (6, None)] '''
    if length < 0:
        return []
    else:
        return [create_tuple(args, length)] + create_list(args, length - 1)

def find_max_index(a_list):
    ''' Find the index of the last element in the list'''
    if not a_list:
        return -1
    else:
        return 1 + find_max_index(a_list[1:])

def find_length(a_list):
    ''' Find the length of an array'''
    if not a_list:
        return 0
    else:
        return 1 + find_length(a_list[1:])

def find_lengths(args):
    ''' Returns a list of all the max indexes amoung all the lists in the tuple'''
    if not args:
        return []
    else:
        return [find_max_index(args[0])] + find_lengths(args[1:])

def find_max(a_list, the_max = None):
    ''' Find the max out of a list '''
    if not a_list:
        return the_max
    else:
        if a_list[0] > the_max:
            the_max = a_list[0]
        return find_max(a_list[1:], the_max)

def simple_map(func, args):
    ''' Maps args to the func'''
    if not args:
        return []
    else:
        return [func(*args[0])] + simple_map(func, args[1:])

def reverse_list(a_list):
    ''' Returns the list in the reverse order'''
    if not a_list:
        return []
    else:
        return reverse_list(a_list[1:]) + [a_list[0]]

def convert_to_type(value, value_type):
    ''' Based on the type of array return the value as an element of that type'''
    if value_type is tuple:
        return (value, )
    elif value_type is str:
        return str(value)
    else:
        return [value]

def fun_map(func, *args):
    ''' Python Map function implementation'''
    return reverse_list(simple_map(func, create_list(args, find_max(find_lengths(args)))))

def fun_reduce(func, array, init = None):
    ''' Python Reduce function implementation'''
    if find_length(array) == 1:
        return array[0]
    else:
        if not init:
            return func(array[0], fun_reduce(func, array[1:]))
        else:
            return func(init, fun_reduce(func, array[1:]))

def fun_filter(func, array):
    ''' Python Filter function implementation'''
    if not array:
        return type(array)()
    if not func:
        return (type(array)() if not array[0] else convert_to_type(array[0], type(array))) + fun_filter(func, array[1:])
    else:
        return (type(array)() if not func(array[0]) else convert_to_type(array[0], type(array))) + fun_filter(func, array[1:])

    if __name__ == '__main__':

        # Test implementation of filter function
        print(fun_filter(lambda x: True if type(x) is str else False, ['unni', 'krishnan', 12]))

        # Test implementation of map function
        print(fun_map(lambda x, y: x + y, [10, 11, 12, 34], [20, 21, 22, 64]))

        # Test implementation of reduce funtion
        print(fun_reduce(lambda x, y: x * y, [1, 2, 3, 4, 5, 6], 10))