


from tornado import gen
from IPython.utils.traitlets import Dict
from jupyterhub.auth import Authenticator
from psycopg2 import pool
import os

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)

JUPYTERHUB_AUTH_METHOD = os.getenv('JUPYTERHUB_AUTH_METHOD', 'Default')

JUPYTER_SERVER_TIMEOUT = os.getenv('SHUTDOWN_NO_ACTIVITY_TIMEOUT', '180')
NOTEBOOK_TIMEOUT = os.getenv('CULL_IDLE_TIMEOUT', '60')

c.JupyterHub.db_url = 'postgresql://{user}:{password}@{host}:{port}/jupyterhub'.format(
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT
)

class KslabAuthenticator(Authenticator):

    passwords = Dict(config=True,
        help="""dict of username:password for authentication"""
    )
    
    pg_pool = pool.ThreadedConnectionPool(
    5, 15, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host=POSTGRES_HOST,
    port=POSTGRES_PORT, database='jupyterhub')
    
    @gen.coroutine
    def authenticate(self, handler, data):
        conn = self.pg_pool.getconn()
        try:
            if conn:
                cur = conn.cursor()
                cur.execute('SELECT * FROM user_passwords WHERE name = %s AND password = %s',
                            (data['username'], data['password']))
                result = cur.fetchone()
                cur.close()
                if result:
                    return data['username']
                else:
                    #self.log.warning(handler.request.remote_ip)
                    self.log.warning("Failed login for %s (@%s)", (data or {}).get('username', 'unknown user'), handler.request.remote_ip)
        finally:
            self.pg_pool.putconn(conn)
        return None

    @gen.coroutine
    def pre_spawn_start(self, user, spawner):
        """Pass upstream_token to spawner via environment variable"""
        auth_state = yield user.get_auth_state()
        if not auth_state:
            # auth_state not enabled
            return
        spawner.environment['UPSTREAM_TOKEN'] = auth_state['upstream_token']


#os.environ['']
#os.environ['OAUTH2_USERDATA_URL'] = "https://portal3g.ncu.edu.tw/apis/oauth/v1/info"
#os.environ['OAUTH2_TOKEN_URL'] = "https://portal3g.ncu.edu.tw/oauth2/token"
#os.environ['OAUTH2_AUTHORIZE_URL'] = "https://portal3g.ncu.edu.tw/oauth2/authorization"
#os.environ['OAUTH2_USERNAME_KEY'] = "identifier"

if JUPYTERHUB_AUTH_METHOD == 'Default':
    c.JupyterHub.authenticator_class = KslabAuthenticator
elif JUPYTERHUB_AUTH_METHOD == 'LTI':
    c.JupyterHub.authenticator_class = 'ltiauthenticator.LTIAuthenticator'
    c.LTIAuthenticator.consumers = {
        os.environ['LTI_CLIENT_KEY']: os.environ['LTI_CLIENT_SECRET']
    }
    c.Authenticator.enable_auth_state = True

#c.JupyterHub.authenticator_class = 'oauthenticator.ncuportal.NCUPortalOAuthenticator'
#c.NCUPortalOAuthenticator.oauth_callback_url = 'https://viscode.moocs.tw/hub/oauth_callback'
#c.NCUPortalOAuthenticator.client_id = '#20190115182958-qzESHNSm'
#c.NCUPortalOAuthenticator.client_secret = 'NJZEujCOqMCTzMn1Ko6VsXDtMCCnPHmIUh9lBbaA078I7pDBC6Tlz1wMUM01Fvxh'
#c.NCUPortalOAuthenticator.scope = ['identifier', 'chinese-name']
## The base URL of the entire application.
#  
#  Add this to the beginning of all JupyterHub URLs. Use base_url to run
#  JupyterHub within an existing website.
#  
#  .. deprecated: 0.9
#      Use JupyterHub.bind_url
#c.JupyterHub.base_url = '/'

# c.JupyterHub.bind_url = 'httpss://0.0.0.0:8000'
c.JupyterHub.cookie_max_age_days = 0.16666
c.JupyterHub.hub_connect_ip = 'jupyterhub'
c.JupyterHub.hub_ip = '0.0.0.0'



## The class to use for spawning single-user servers.
#  
#  Should be a subclass of Spawner.
#c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# c.DockerSpawner.image = 'jupyter/scipy-notebook:87210526f381'
# c.DockerSpawner.image = 'jupyter/scipy-notebook:latest'
c.DockerSpawner.image = 'viscode-jupyter:latest'

#c.DockerSpawner.host_ip = "127.0.0.1"
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = { '/jupyterhub_users/{username}': notebook_dir }
c.DockerSpawner.remove = True
c.DockerSpawner.environment = {
    'VISCODE_API_SERVER_HOST' : 'viscode-api',
    'VISCODE_API_SERVER_PORT' : 80,
    'JUPYTERHUB_AUTH_METHOD': JUPYTERHUB_AUTH_METHOD
}
c.DockerSpawner.extra_create_kwargs = {
#    'network_disabled' : True
}

c.DockerSpawner.extra_host_config = {
    'pids_limit' : 400,
    'device_read_bps': [{'Path': '/dev/sda', 'Rate': 60*1024*1024}],
    'device_write_bps': [{'Path': '/dev/sda', 'Rate': 10*1024*1024}],
    'device_read_iops': [{'Path': '/dev/sda', 'Rate': 100}],
    'device_write_iops': [{'Path': '/dev/sda', 'Rate': 60}],
    'network_mode': 'viscode_viscode'
}
c.DockerSpawner.network_name = 'viscode_viscode'
#c.DockerSpawner.network_name = 'no-internet'
#c.DockerSpawner.use_internal_ip = False
c.DockerSpawner.use_internal_ip = True

# 限制 CPU
c.Spawner.cpu_limit = 2

# 限制記憶體
c.Spawner.mem_limit = '2G'

c.Spawner.http_timeout = 180

# 節省資源，自動關閉閒置的 notebook 與 container
c.Spawner.args = [
    '--MappingKernelManager.cull_idle_timeout=' + NOTEBOOK_TIMEOUT,
    '--NotebookApp.shutdown_no_activity_timeout=' + JUPYTER_SERVER_TIMEOUT 
]


import subprocess
def create_dir_hook(spawner):
    user_dir = os.path.join('/jupyterhub_users', spawner.escaped_name)
    # user_course_dir = os.path.join(user_dir, '課程')
    # hw1 = []
    # hw2 = []
    # hw3 = []
    # for i in range(1, 6):
    #     hw1.append(os.path.join(user_course_dir, '{}_HW1_{}.ipynb'.format(spawner.user.name[4:], i)))
    # for i in range(1, 5):
    #     hw2.append(os.path.join(user_course_dir, '{}_HW2_{}.ipynb'.format(spawner.user.name[4:], i)))
    # for i in range(1, 7):
    #     hw3.append(os.path.join(user_course_dir, '{}_HW3_{}.ipynb'.format(spawner.user.name[4:], i)))
    if not os.path.exists(user_dir):
        os.mkdir(user_dir)
        os.chown(user_dir, 1000, 100)
        # os.chmod(notebook_dir, 0o675)
    # if not os.path.exists(user_course_dir):
    #     os.mkdir(user_course_dir)
    # os.chown(user_course_dir, 999, 100)
    # os.chmod(user_course_dir, 0o677)
    # for hw in hw1:
    #     if not os.path.exists(hw):
    #         with open(hw, 'w') as f:
    #             f.write('{"cells": [],"metadata": {},"nbformat": 4, "nbformat_minor": 2}')
    #             f.close()
    #     os.chmod(hw, 0o677)
    #     os.chown(hw, 1000, 100)
    # for hw in hw2:
    #     if not os.path.exists(hw):
    #         with open(hw, 'w') as f:
    #             f.write('{"cells": [],"metadata": {},"nbformat": 4, "nbformat_minor": 2}')
    #             f.close()
    #     os.chmod(hw, 0o677)
    #     os.chown(hw, 1000, 100)
    # for hw in hw3:
    #     if not os.path.exists(hw):
    #         with open(hw, 'w') as f:
    #             f.write('{"cells": [],"metadata": {},"nbformat": 4, "nbformat_minor": 2}')
    #             f.close()
    #     os.chmod(hw, 0o677)
    #     os.chown(hw, 1000, 100)
    #    subprocess.call(["sudo", "-u", 'kslab', 'mkdir', '-p', user_dir])
    #if not os.path.exists(user_course_dir):
    #    subprocess.call(["sudo", 'mkdir', '-p', user_course_dir])

c.Spawner.pre_spawn_hook = create_dir_hook

## Extra settings overrides to pass to the tornado application.
c.JupyterHub.tornado_settings = {}
c.JupyterHub.tornado_settings['cookie_options'] = {
    'expires_days': 0.16666,
}




c.Authenticator.admin_users = { 'admin', 'ncu_107522012' }


c.Authenticator.blacklist = { 'ncu_107502004' }
