import tornado.httpclient
import json
import requests
import os
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler
from tornado.web import RequestHandler

class UserAccessRolesHandler(IPythonHandler):
    
    SUPPORTED_METHODS = ('GET', 'POST', 'PATCH')
    
    def initialize(self, mylog=None):
        self.mylog = mylog
        self.viscode_api_host = os.getenv('VISCODE_API_SERVER_HOST', '127.0.0.1')
        self.viscode_api_port = os.getenv('VISCODE_API_SERVER_PORT', 5000)

    @tornado.web.asynchronous
    def get(self):
        role = None
        isAdmin = self.get_current_user()['admin']

        if isAdmin == True:
            role = 'admin'

        self.finish(json.dumps({
            'role': role
        }))

    @tornado.web.asynchronous
    def post(self):
        post_data = json.loads(self.request.body.decode('utf-8'))
        account = post_data.get('account', None)
        password = post_data.get('password', None)
        session_id = self.get_cookie('jupyterhub-session-id')
        
        if account is None or password is None:
            self.send_error(400)
        elif session_id:
            data = {
                'sessionId' : session_id,
                'account' : account,
                'password': password
            }
            r = requests.post('http://{}:{}/users'.format(self.viscode_api_host, self.viscode_api_port), json=data)
            res_data = r.json()

            if 'isError' in res_data and res_data['isError'] == True:
                if 'msg' in res_data:
                    self.finish(json.dumps({
                        'msg': res_data['msg'],
                        'isError': True
                    }))
                else:
                    self.finish(json.dumps({
                        'msg': 'API server error!',
                        'isError': True
                    }))
            else:
                self.finish(json.dumps({
                    'msg': 'success',
                    'isError': False
                }))
        else:
            self.send_error(400)

    @tornado.web.asynchronous
    def patch(self):
        post_data = json.loads(self.request.body.decode('utf-8'))
        account = post_data.get('account', None)
        password = post_data.get('password', None)
        session_id = self.get_cookie('jupyterhub-session-id')
        
        if account is None or password is None:
            self.send_error(400)
        elif session_id:
            data = {
                'sessionId' : session_id,
                'account' : account,
                'password': password
            }
            r = requests.patch('http://{}:{}/users/{}'.format(self.viscode_api_host, self.viscode_api_port, account), json=data)
            res_data = r.json()

            if 'isError' in res_data and res_data['isError'] == True:
                if 'msg' in res_data:
                    self.finish(json.dumps({
                        'msg': res_data['msg'],
                        'isError': True
                    }))
                else:
                    self.finish(json.dumps({
                        'msg': 'API server error!',
                        'isError': True
                    }))
            else:
                self.finish(json.dumps({
                    'msg': 'success',
                    'isError': False
                }))
        else:
            self.send_error(400)

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
        (ujoin(base_url, r"/viscode/users"), UserAccessRolesHandler,
            {'mylog': nbapp.log}),
    ])
