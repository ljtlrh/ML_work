#!/usr/bin/env python
# encoding=utf-8

import tornado.web
from tornado.web import URLSpec
from tornado.ioloop import IOLoop
import numpy as np

from handler_helper import *

import tornado.httpserver
import tornado.ioloop
import tornado.web

from tornado.options import define,options

define('port',default=8000,help='run port',type=int)
login_key = ''
class AuthError(Exception):
    def __init__(self,msg):
        super(AuthError,self).__init__(msg)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        username = 'no'
        self.render('templates/index.html',username=username)

class LoginHandler(tornado.web.RequestHandler):    #登录
    def get(self):
        self.render('templates/login.html',error=None)
    def post(self):
        username = self.get_argument('name','')
        passwd = self.get_argument('password','')
        login_key = np.random.rand()
        if username == "admin" and passwd == "123456":
            self.render('templates/index.html',
                        username=username,
                        key=login_key
                        )
        else:
            self.render('login.html',error='登陆失败')

class RegisterHandler(tornado.web.RequestHandler):   #注册
    def get(self):
        self.render('08register.html',error=None)

    def post(self):
        if self._check_argument():
            try:
                self._create_user()
                self.render('08login.html',error=None)
            except AuthError as e:
                self.render('08register.html',error=e)
            except Exception as e:
                self.render('08register.html',error=e)
        else:
            self.render('08register.html',error='input error')

    def _check_argument(self):      #对密码和用户名进行检验
        username = self.get_argument('name','')
        passwd = self.get_argument('password1','')
        if len(username)<10 and len(passwd)<10:
            return True
        else:
            return False


HANDLERS = [
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),
    URLSpec(r'/api/hadoop/monitor/logger', APIMonitorHandler,
            name=APIMonitorHandler.__name__),
            (r'/', IndexHandler),
            (r'/login', LoginHandler),
            (r'/register', RegisterHandler),
]

if __name__ == '__main__':
    import sys
    SERVER_PORT = 7100 if len(sys.argv) < 2 else int(sys.argv[1])

    app = tornado.web.Application(HANDLERS, debug=True)
    app.listen(SERVER_PORT, address='0.0.0.0')
    print('tornado server started on port {port}'.format(port=SERVER_PORT))
    IOLoop.current().start()
