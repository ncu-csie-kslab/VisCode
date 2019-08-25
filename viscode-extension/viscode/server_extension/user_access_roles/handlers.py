import tornado.httpclient
import json
import requests
import os
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler
from tornado.web import RequestHandler
from tornado import gen

class UserAccessRolesHandler(IPythonHandler):
    
    SUPPORTED_METHODS = ['GET', 'POST', 'PUT']
    
    def initialize(self, mylog=None):
        self.mylog = mylog
        self.viscode_api_host = os.getenv('VISCODE_API_SERVER_HOST', '127.0.0.1')
        self.viscode_api_port = os.getenv('VISCODE_API_SERVER_PORT', 5000)

    @gen.coroutine
    def get(self):
        role = None
        isAdmin = self.get_current_user()['admin']

        if isAdmin == True:
            role = 'admin'

        self.finish(json.dumps({
            'role': role
        }))

    def check_xsrf_cookie(self):
        '''
        http://www.tornadoweb.org/en/stable/guide/security.html
        Defer to proxied apps.
        '''
        pass

def load_jupyter_server_extension(nbapp):

    webapp = nbapp.web_app
    base_url = webapp.settings['base_url']
    webapp.add_handlers(".*$", [
        (ujoin(base_url, r"/viscode/role"), UserAccessRolesHandler,
            {'mylog': nbapp.log}),
    ])
