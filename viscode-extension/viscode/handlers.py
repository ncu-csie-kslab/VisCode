import tornado.httpclient
import json
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler
from tornado.web import RequestHandler

class MyLogHandler(IPythonHandler):
    
    SUPPORTED_METHODS = ['GET', 'POST', 'PUT']
    
    def initialize(self, mylog=None):
        self.mylog = mylog    

    @tornado.web.asynchronous
    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        
        username = self.get_current_user()['name']

        log_data = {
            'username': username,
            'event': 'code_execution',
        }
        # self.mylog.info(data)
        if data['isError'] == True:
            log_data['isError'] = True
            log_data['errorName'] = data['errorName']
            self.log.info('{} | {} '.format(username, data['errorName']))
        else :
            log_data['isError'] = False
            self.log.info('{} | {}'.format(username, 'Pass'))
        self.finish()

    def check_xsrf_cookie(self):
        '''
        http://www.tornadoweb.org/en/stable/guide/security.html
        Defer to proxied apps.
        '''
        pass

def setup_handlers(nbapp):
    nbapp.log.info('SciPy Ext loaded')

    webapp = nbapp.web_app
    base_url = webapp.settings['base_url']
    webapp.add_handlers(".*$", [
        (ujoin(base_url, r"/scipy/log"), MyLogHandler,
            {'mylog': nbapp.log}),
    ])
