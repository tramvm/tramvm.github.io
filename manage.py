#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from gevent import monkey
monkey.patch_all()

import grpc.experimental.gevent as grpc_gevent
grpc_gevent.init_gevent()

from flask.ext.script import Manager
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from inside import create_app

#from inside import inside
#from werkzeug.wsgi import DispatcherMiddleware

sys.path.pop(0)
sys.path.insert(0, os.getcwd())

def set_procname(newname):
    from cffi import FFI
    ffi = FFI()
    C = ffi.cdef("""
        int prctl(int option, ...);
        """)
    C = ffi.dlopen(None)
    return C.prctl(15, ffi.new("char[]", newname))


app = create_app()
manager = Manager(app)
#app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {'/inside': inside})

project_root_path = os.path.join(os.path.dirname(app.root_path))


@manager.command
def run():
    """Run local server."""
#    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {'/inside': inside})
    app.run(host='0.0.0.0',port=9881)


@manager.command
def gevent():
    """Run with gevent WSGI Server"""
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    #from socketio.server import SocketIOServer
    #SocketIOServer(('0.0.0.0', 5000), app,
    #    namespace="socket.io", policy_server=False).serve_forever()


@manager.command
def urls():
    print app.url_map


@manager.command
def babel():
    cmd = 'pybabel update -i messages.pot -d translations'
    import commands
    commands.getstatusoutput(cmd)

@manager.command
def tornado():
    set_procname('inside')
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
#    http_server.bind(5000)
#    http_server.start(0)  # Forks multiple sub-processes
    IOLoop.instance().start()

@manager.command
def meinheld():
    from meinheld import server
#    patch.patch_all()

    server.listen(("0.0.0.0", 8000))
    server.run(app)
#    http_server.bind(5000)
#    http_server.start(0)  # Forks multiple sub-processes
   # IOLoop.instance().start()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
    #app.run(port=4999)
