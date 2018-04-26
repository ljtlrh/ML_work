#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author:
@contact:
@site: 
@software: PyCharm
@file: py_hdaoop_monitor01.py
@time: 18-4-24 下午5:18
"""
import time
import threading
import pycurl
import io
import re
import json


st=0

def time_count():
    global st
    i=10
    while i>0:
        i-=1
        time.sleep(1)
        if st==1:
            st=0
            return

    # print "there is no running task"


def check_state():
    st_num=0
    b = io.StringIO()
    c = pycurl.Curl()
    checkurl = "http://192.168.31.10:8088/ws/v1/cluster/apps" #需要监控的地址
    c.setopt(pycurl.URL, checkurl)
    c.setopt(pycurl.HTTPHEADER, ["Accept:"])
    c.setopt(pycurl.WRITEFUNCTION, b.write) #回调
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 5) #重定向
    c.setopt(pycurl.CONNECTTIMEOUT, 60) #链接超时
    c.perform() #运行
    status = c.getinfo(c.HTTP_CODE)

    html = b.getvalue()

    dic_a=json.loads(html)
    dic_b=dic_a['apps']                  #dic_b=second dic
    if dic_b!=None:                  #没有作业时，列表为空,非空才可获取
        list_c=dic_b['app']              #list_c= thrid liebiao
        for dic_d in list_c:             #dic_d= fourth dic
            if dic_d['state']=='FINISHED':
                st_num+=1
        if st_num==len(list_c):          # 所有作业finished
            return 0
        else:
            return 1

    else:
        return 0

    c.close()
    b.close()

def aaa():
    import urllib

    url = "http://192.168.31.10:50070/jmx?qry=Hadoop:service=NameNode,name=NameNodeInfo"
    page = urllib.urlopen(url)
    html = page.read()

    reg = r'“state”:[A-Z]*'
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    for content in imglist:
        print (content)

if __name__ == '__main__':
    aaa()

    t1=threading.Thread(target=time_count)
    pnum=0;
    while True:
        pnum+=1
        print ('check state %d\n'%pnum)
        re_state=check_state()
        if re_state==0:                                        #no task is running :
            if t1.is_alive() ==False:
                t1=threading.Thread(target=time_count)
                t1.start()
        if re_state==1:                                        # task is running :
            if t1.is_alive() ==True:
                st=1                                   #shutdown thread
        #other program
        time.sleep(1)


    #other program