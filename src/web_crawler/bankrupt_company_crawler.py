#!/usr/bin/env python
# -*- coding:utf-8 -*-  
"""
@version: python2.7
@author: ‘liujiantao‘ 
@contact: 
@site: 
@software: PyCharm
@file: bankrupt_company_crawler.py
@time: 18-6-5 上午10:35
"""
import sys
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import request
import re
import requests


def get_company_names01(path):
    """
    读取txt文本
    :param path:
    :return:
    """
    company_names = []
    with open(path) as f:
        for data in f.readlines():
            if data.startswith('#'):
                continue
            name = data.decode('utf-8')
            # print name
            company_names.append(name.strip("\n"))
    return company_names

bankrupt_company_list01 = get_company_names01(
    "/home/sinly/ljtstudy/code/ML_work/src/pysaprk_demo/data/bankrupt_company_ok.txt")


def is_none(d):
    return (d is None or d == 'None' or
            d == '?' or
            d == '' or
            d == 'NULL' or
            d == 'null')

def get_isca(url, headers, payload):
    bankrupt_list = []
    page = requests.post(url, data=payload, headers=headers).text
    soup = BeautifulSoup(page, 'html5lib')
    ul_li_list = soup.select('body')[0].select('ul')[0].select('li')
    for li_tag in ul_li_list:
        S = li_tag.text.replace('\t', '').replace('\n', '').replace(' ', '')
        if "破产公告" in S or "破产文书" in S:
            po1 = S.find("裁定受理")
            po2 = S.find("破产清算")
            if po1 < 0 or po2 < 0:
                po1 = S.find("被申请人：")
                po2 = S.find("公司")
                if po1 < 0 or po2 < 0: continue
                company_name = S[po1 + 5:po2 + 2].replace('\t', '').replace('\n', '').replace(' ', '')
                if is_none(company_name): continue
                bankrupt_list.append(company_name)
                continue
            company_name = S[po1 + 4:po2].strip(" ")
            if is_none(company_name): continue
            if "公司" not in company_name:
                company_name = company_name.replace('公', '公司')
            bankrupt_list.append(company_name.replace('\t', '').replace('\n', '').replace(' ', ''))
    return list(set(bankrupt_list))




# def soup_parser(soup):


    # # 输出第一个 title 标签
    # print soup.title
    #
    # # 输出第一个 title 标签的标签名称
    # print soup.title.name
    #
    # # 输出第一个 title 标签的包含内容
    # print soup.title.string
    #
    # # 输出第一个 title 标签的父标签的标签名称
    # print soup.title.parent.name
    #
    # # 输出第一个  p 标签
    # print soup.p
    #
    # # 输出第一个  p 标签的 class 属性内容
    # print soup.p['class']
    #
    # # 输出第一个  a 标签的  href 属性内容
    # print soup.a['href']
    # '''''
    # soup的属性可以被添加,删除或修改. 再说一次, soup的属性操作方法与字典一样
    # '''
    # # 修改第一个 a 标签的href属性为 http://www.baidu.com/
    # soup.a['href'] = 'http://www.baidu.com/'
    #
    # # 给第一个 a 标签添加 name 属性
    # soup.a['name'] = u'百度'
    #
    # # 删除第一个 a 标签的 class 属性为
    # del soup.a['class']
    #
    # ##输出第一个  p 标签的所有子节点
    # print soup.p.contents
    #
    # # 输出第一个  a 标签
    # print soup.a
    #
    # # 输出所有的  a 标签，以列表形式显示
    # print soup.find_all('a')
    #
    # # 输出第一个 id 属性等于  link3 的  a 标签
    # print soup.find(id="link3")
    #
    # # 获取所有文字内容
    # print(soup.get_text())
    #
    # # 输出第一个  a 标签的所有属性信息
    # print soup.a.attrs
    #
    # for link in soup.find_all('a'):
    #     # 获取 link 的  href 属性内容
    #     print(link.get('href'))
    #
    #     # 对soup.p的子节点进行循环输出
    # for child in soup.p.children:
    #     print(child)
    #
    #     # 正则匹配，名字中带有b的标签
    # for tag in soup.find_all(re.compile("li")):
    #     print(tag.name)


    #解析最外层
def blogParser(index):

  cnblogs = request.requestCnblogs(index)
  soup = BeautifulSoup(cnblogs, 'html.parser')
  all_div = soup.find_all('div', attrs={'class': 'post_item_body'}, limit=20)

  blogs = []
  #循环div获取详细信息
  for item in all_div:
      blog = analyzeBlog(item)
      blogs.append(blog)

  return blogs

#解析每一条数据
def analyzeBlog(item):
    result = {}
    a_title = find_all(item,'a','titlelnk')
    if a_title is not None:
        # 博客标题
        result["title"] = a_title[0].string
        # 博客链接
        result["href"] = a_title[0]['href']
    p_summary = find_all(item,'p','post_item_summary')
    if p_summary is not None:
        # 简介
        result["summary"] = p_summary[0].text
    footers = find_all(item,'div','post_item_foot')
    footer = footers[0]
    # 作者
    result["author"] = footer.a.string
    # 作者url
    result["author_url"] = footer.a['href']
    str = footer.text
    time = re.findall(r"发布于 .+? .+? ", str)
    result["create_time"] = time[0].replace('发布于 ','')

    comment_str = find_all(footer,'span','article_comment')[0].a.string
    result["comment_num"] = re.search(r'\d+', comment_str).group()

    view_str = find_all(footer,'span','article_view')[0].a.string
    result["view_num"] = re.search(r'\d+', view_str).group()

    return result

def find_all(item,attr,c):
    return item.find_all(attr,attrs={'class':c},limit=1)


def get_bankrupt_company_name(company_name):
    """

    :param company_name:
    :return:
    """
    company_names = []
    try:
        url = 'http://pccz.court.gov.cn/pcajxxw/searchKey/qzsslb'
        headers = {
            "Accept": 'text/html,*/*;q = 0.01',
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "zh-CN,zh;q = 0.9",
            "Connection": "keep-alive",
            "Content-Length": "112",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Host": "pccz.court.gov.cn",
            "Origin": "http://pccz.court.gov.cn",
            "Referer": "http://pccz.court.gov.cn/pcajxxw/searchKey/qzss",
            "X-Requested-With": "XMLHttpRequest"
        }
        payload = {
            'gjz': company_name
        }
        company_names = get_isca(url, headers, payload)
    except Exception as e:
        traceback.print_exc()
    return company_names



if __name__ == '__main__':
    import json
    bankrupt_company = []
    i = 0
    for company in bankrupt_company_list01:
        i += 1
        companys = get_bankrupt_company_name(company)
        bankrupt_company.extend(companys)
        print(i)
    bankrupt_company = list(set(bankrupt_company))
    print(bankrupt_company.__len__())
    print (json.dumps(bankrupt_company, ensure_ascii=False, indent=4))
    f1 = open('/home/sinly/ljtstudy/code/ML_work/src/pysaprk_demo/data/bankrupt_company_ok01.txt', 'w')
    for company in bankrupt_company:
        company = company+"\n"
        f1.write(company)
    f1.flush()
    f1.close()
