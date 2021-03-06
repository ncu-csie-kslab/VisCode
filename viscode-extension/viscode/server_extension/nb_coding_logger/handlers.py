import tornado.httpclient
import json
import requests
import os
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler
from tornado.web import RequestHandler
from tornado import gen
from viscode.utils import get_default_log

class CodingLoggerHandler(IPythonHandler):
    
    SUPPORTED_METHODS = ['GET', 'POST', 'PUT']
    
    def initialize(self, mylog=None):
        self.mylog = mylog
        self.viscode_api_host = os.getenv('VISCODE_API_SERVER_HOST', '127.0.0.1')
        self.viscode_api_port = os.getenv('VISCODE_API_SERVER_PORT', 5000)

    @gen.coroutine
    def post(self):
        post_data = json.loads(self.request.body.decode('utf-8'))
        events = ['code_execution', 'code_copy', 'code_paste', 'code_speed']
        username = self.get_current_user()['name']

        if post_data['event'] in events:
            log_data = get_default_log()
            log_data.update({
                'username': username
            })
            log_data.update(post_data)
            
            requests.post('http://{}:{}/logs'.format(self.viscode_api_host, self.viscode_api_port), json=log_data)
        self.finish()

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
        (ujoin(base_url, r"/viscode/coding_logs"), CodingLoggerHandler,
            {'mylog': nbapp.log}),
    ])
