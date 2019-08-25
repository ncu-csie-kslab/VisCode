import tornado.httpclient
import json
import requests
import os
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler
from tornado.web import RequestHandler
from tornado import gen

class TreeAnnouncementsHandler(IPythonHandler):
    
    SUPPORTED_METHODS = ['GET', 'POST']
    
    def initialize(self, mylog=None):
        self.mylog = mylog
        self.viscode_api_host = os.getenv('VISCODE_API_SERVER_HOST', '127.0.0.1')
        self.viscode_api_port = os.getenv('VISCODE_API_SERVER_PORT', 5000)

    @gen.coroutine
    def get(self):
        # role = None
        # isAdmin = self.get_current_user()['admin']

        # if isAdmin == True:
        #     role = 'admin'

        r = requests.get('http://{}:{}/announcement'.format(self.viscode_api_host, self.viscode_api_port))
        data = r.json()

        self.finish(json.dumps(data))

    @gen.coroutine
    def post(self):
        post_data = json.loads(self.request.body.decode('utf-8'))
        announcement_type = post_data.get('type', None)
        announcement_text = post_data.get('text', None)
        session_id = self.get_cookie('jupyterhub-session-id')

        if announcement_type is None or announcement_text is None:
            self.send_error(400)
        elif session_id:
            data = {
                'sessionId' : session_id,
                'type' : announcement_type,
                'text': announcement_text
            }
            r = requests.post('http://{}:{}/announcement'.format(self.viscode_api_host, self.viscode_api_port), json=data)
            res_data = r.json()

            if 'isError' in res_data and res_data['isError']:
                 self.finish(json.dumps({
                    'msg': 'API server error!',
                    'isError': True
                }))

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
        (ujoin(base_url, r"/viscode/announcement"), TreeAnnouncementsHandler,
            {'mylog': nbapp.log}),
    ])
