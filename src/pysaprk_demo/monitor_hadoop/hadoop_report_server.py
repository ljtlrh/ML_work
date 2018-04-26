#!/usr/bin/env python
# encoding=utf-8

import sys

import tornado.web
from tornado.web import URLSpec
from tornado.ioloop import IOLoop

from scpy.logger import get_logger

from handler_helper import *

reload(sys)
sys.setdefaultencoding('utf-8')

logger = get_logger(__file__)

HANDLERS = [
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static/'}),

    URLSpec(r'/api/hadoop/monitor/logger', APIMonitorHandler,
            name=APIMonitorHandler.__name__),

]

if __name__ == '__main__':
    SERVER_PORT = 7100 if len(sys.argv) < 2 else int(sys.argv[1])

    app = tornado.web.Application(HANDLERS, debug=True)
    app.listen(SERVER_PORT, address='0.0.0.0')
    logger.info('tornado server started on port {port}'.format(port=SERVER_PORT))
    IOLoop.current().start()
