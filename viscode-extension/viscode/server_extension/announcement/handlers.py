import tornado.httpclient
import json
from notebook.utils import url_path_join as ujoin
from notebook.base.handlers import IPythonHandler
from tornado import web

class SurveyHandler(IPythonHandler):

    SUPPORTED_METHODS = ['GET', 'POST']

    @web.authenticated
    def get(self):
        # data = json.loads(self.request.body.decode('utf-8'))
        data = {'isError': False}

        name = self.get_current_user()['name']
        is_admin = self.get_current_user()['admin']
        survey_id = self.get_argument('id')

        result = survey.find_one({'_id': ObjectId(survey_id)})

        data['survey'] = result
        self.finish(dumps(data))

    @web.authenticated
    def post(self):
        data = {'isError': False}
        report_data = {}
        try:
            name = self.get_current_user()['name']
            isAdmin = self.get_current_user()['admin']
            # self.log.info(self.request.arguments)
            survey_id = self.get_argument('id')
            survey_data = survey.find_one({'_id': ObjectId(survey_id)})
            # self.log.info(self.request.body.decode('utf-8'))
            data = json.loads(self.request.body.decode('utf-8'))
            blocks = survey_data['blocks']

            for item in data['formData']:
                index = int(item['name'])
                value = item['value']
                block = blocks[index]

                if block['type'] == 'text':
                    block['answer'] = value
                elif block['type'] == 'number':
                    block['answer'] = value
                elif block['type'] == 'choice':
                    select = int(value)
                    block['select'] = select
                    block['answer'] = block['options'][select]['text']
            report_data['title'] = survey_data['title']
            report_data['userId'] = name
            report_data['surveyId'] = ObjectId(survey_id)
            report_data['blocks'] = blocks
            report_data['events'] = data['events']
            report_data['surveyShowTime'] = data['surveyShowTime']
            report_data['surveyCloseTime'] = data['surveyCloseTime']
            report_data['surveyStartEditTime'] = data['surveyStartEditTime']

            report.update_one({'surveyId': ObjectId(survey_id), 'userId': name}, {
                '$set': report_data,
                '$currentDate': {
                    'createdAt': {'$type': 'date'},
                    'updatedAt': {'$type': 'date'}
                }
            }, upsert=True)

        except web.MissingArgumentError:
            data['isError'] = True
            data['msg'] = 'Missing argument error!'
        finally:
            self.finish(dumps(data))

    # @tornado.web.asynchronous
    # def put(self):
    #     data = json.loads(self.request.body.decode('utf-8'))
    #     username = self.get_current_user()['name']
    # self.mylog.info(data)
    #     if data['isError'] == True:
    #         self.log.info('{} | {} '.format(username, data['errorName']))
    #     else :
    #         self.log.info('{} | {}'.format(username, 'Pass'))
    #     self.finish()

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
        (ujoin(base_url, r"/survey/survey"), SurveyHandler),
        (ujoin(base_url, r"/survey/report"), ReportHandler),
        (ujoin(base_url, r"/survey/reports"), ReportsHandler),
        (ujoin(base_url, r"/survey/peerreview"), PeerReviewSurveyHandler),
    ])
