#!/usr/bin/env python
# -*- coding:utf-8 -*- 
# @Time    : 18-3-23 下午5:58
# @Author  : liujiantao
# @Site    : 
# @File    : send_emails_utils.py
# @Software: PyCharm
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.utils import parseaddr, formataddr

import smtplib

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

'''加密发送文本邮件'''
def sendEmail(from_addr,password,to_addr,smtp_server):
    try:
        msg = MIMEText(' 测试...', 'plain', 'utf-8') # 文本邮件
        # msg = MIMEText('<html><body><h1>你好</h1>' + '<p>send by <a href="http://www.python.org">
        #         信息化工程所</a>...</p>' +'</body></html>', 'html', 'utf-8') # 网页文件

        msg['From'] = _format_addr('信息化工程所 <%s>' % from_addr)
        msg['To'] = _format_addr('收件人 <%s>' % to_addr)
        msg['Subject'] = Header('邮件的主题：问候', 'utf-8').encode()

        server = smtplib.SMTP(smtp_server, 25)
        server.starttls() # 调用starttls()方法，就创建了安全连接
        # server.set_debuglevel(1) # 记录详细信息
        server.login(from_addr, password) # 登录邮箱服务器
        server.sendmail(from_addr, [to_addr], msg.as_string()) # 发送信息
        server.quit()
        print("加密后邮件发送成功！")
    except Exception as e:
        print("发送失败：" + e)


'''发送带图片附件的邮件'''
def sendFileEmail(from_addr,password,to_addr,smtp_server):
    try:
        msg =  MIMEMultipart()
        msg['From'] = _format_addr('信息化工程所 <%s>' % from_addr)
        msg['To'] = _format_addr('收件人 <%s>' % to_addr)
        msg['Subject'] = Header('邮件的主题：问候', 'utf-8').encode()
        # 邮件正文是MIMEText:
        msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
        # msg.attach(MIMEText('<html><body><h1>你好</h1>' + '<p>send by <img src=cid:0"></p>' +'</body></html>', 'html', 'utf-8')) # 网页文件


        # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
        with open(r'./file/图片.png', 'rb') as f:
            mime = MIMEBase('image', 'png', filename='图片.png') # 设置附件的MIME和文件名，这里是png类型:
            mime.add_header('Content-Disposition', 'attachment',filename=('gbk', '', '图片.png')) # 加上必要的头信息,解决中文附件名乱码
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            mime.set_payload(f.read())  # 把附件的内容读进来:
            encoders.encode_base64(mime) # 用Base64编码:
            msg.attach(mime) # 添加到MIMEMultipart:

        server = smtplib.SMTP(smtp_server, 25)
        # server.set_debuglevel(1) # 记录详细信息
        server.login(from_addr, password) # 登录邮箱服务器
        server.sendmail(from_addr, to_addr, msg.as_string()) # 发送信息
        server.quit()
        print("带图片邮件发送成功！")
    except Exception as e:
        print("发送失败：" + e)



'''发送带图片附件的邮件'''
def sendFilesEmail(from_addr,password,to_addr,smtp_server):
    try:
        msg =  MIMEMultipart()
        msg['From'] = _format_addr('信息化工程所 <%s>' % from_addr)
        msg['To'] = _format_addr('收件人 <%s>' % to_addr)
        msg['Subject'] = Header('邮件的主题：问候', 'utf-8').encode()
        # 邮件正文是MIMEText:
        msg.attach(MIMEText('发送多附件邮件...', 'plain', 'utf-8'))

        #---这是附件部分---
        #xlsx类型附件
        part = MIMEApplication(open(r'./file/foo.xlsx','rb').read())
        part.add_header('Content-Disposition', 'attachment', filename="foo.xlsx")
        msg.attach(part)

        #jpg类型附件
        part = MIMEApplication(open(r'./file/图片.png','rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=('gbk', '', '图片.png'))
        msg.attach(part)

        #pdf类型附件
        part = MIMEApplication(open(r'./file/foo.pdf','rb').read())
        part.add_header('Content-Disposition', 'attachment', filename="foo.pdf")
        msg.attach(part)

        # #mp3类型附件
        # part = MIMEApplication(open('foo.mp3','rb').read())
        # part.add_header('Content-Disposition', 'attachment', filename="foo.mp3")
        # msg.attach(part)

        server = smtplib.SMTP(smtp_server, 25,timeout=30)
        # server.set_debuglevel(1) # 记录详细信息
        server.login(from_addr, password) # 登录邮箱服务器
        server.sendmail(from_addr, to_addr, msg.as_string()) # 发送信息
        server.quit()
        print("带图片邮件发送成功！")
    except Exception as e:
        print("发送失败：" + e)



if __name__ == '__main__':
    from_addr = "socialcredicts@163.com"   # 邮箱登录用户名
    password = '1socialcredits1'              # 登录密码
    to_addr = ["jiantao.liu@socialcredits.cn", "yuanjiang.huang@socialcredits.cn"]                                    # 发送对象地址，可以多个邮箱
    smtp_server='smtp.163.com'          # 服务器地址，默认端口号25
    sendEmail(from_addr,password,to_addr,smtp_server)