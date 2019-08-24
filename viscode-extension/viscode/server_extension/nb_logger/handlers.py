import tornado.httpclient
import json
import requests
import os
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler
from tornado.web import RequestHandler

class NotebookLoggerHandler(IPythonHandler):
    
    SUPPORTED_METHODS = ['GET', 'POST', 'PUT']
    
    def initialize(self, mylog=None):
        self.mylog = mylog
        self.viscode_api_host = os.getenv('VISCODE_API_SERVER_HOST', '127.0.0.1')
        self.viscode_api_port = os.getenv('VISCODE_API_SERVER_PORT', 5000)

    @tornado.web.asynchronous
    def post(self):
        post_data = json.loads(self.request.body.decode('utf-8'))
        
        username = self.get_current_user()['name']

        log_data = {
            'username': username,
            'event': 'notebook_open',
        }
        log_data.update(post_data)
        
        # self.mylog.info(data)
        # if data['isError'] == True:
        #     log_data['isError'] = True
        #     log_data['errorName'] = data['errorName']
        #     self.log.info('{} | {} '.format(username, data['errorName']))
        # else :
        #     log_data['isError'] = False
        #     self.log.info('{} | {}'.format(username, 'Pass'))
        # print(self.viscode_api_host, ' ', self.viscode_api_port)

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
        (ujoin(base_url, r"/viscode/nb_logs"), NotebookLoggerHandler,
            {'mylog': nbapp.log}),
    ])
