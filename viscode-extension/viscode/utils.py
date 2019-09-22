import os

JUPYTERHUB_AUTH_METHOD = os.getenv('JUPYTERHUB_AUTH_METHOD')

LTI_CONTEXT_TITLE = os.getenv('LTI_CONTEXT_TITLE')
LTI_CONTEXT_LABEL = os.getenv('LTI_CONTEXT_LABEL')
LTI_CONTEXT_ID = os.getenv('LTI_CONTEXT_ID')
LTI_EMAIL = os.getenv('LTI_EMAIL')
LTI_FIRSTNAME = os.getenv('LTI_FIRSTNAME')
LTI_LASTNAME = os.getenv('LTI_LASTNAME')
LTI_NAME = os.getenv('LTI_NAME')
LTI_USERNAME = os.getenv('LTI_USERNAME')
LTI_LOCALE = os.getenv('LTI_LOCALE')
LTI_ROLES = os.getenv('LTI_ROLES')

def add_lti_to_log(log):
    lti = {
        'lti': {
            'contextId': LTI_CONTEXT_ID,
            'contextTitle': LTI_CONTEXT_TITLE,
            'contextLable': LTI_CONTEXT_LABEL,
            'firstName': LTI_FIRSTNAME,
            'lastName': LTI_LASTNAME,
            'name': LTI_NAME,
            'username': LTI_USERNAME,
            'email': LTI_EMAIL,
            'roles': LTI_ROLES,
            'locale': LTI_LOCALE
        }
    }
    log.update(lti)

def get_default_log():
    log = {}
    if JUPYTERHUB_AUTH_METHOD == 'LTI':
        add_lti_to_log(log)
    return log
