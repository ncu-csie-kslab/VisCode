FROM jupyterhub/jupyterhub:1.0.0
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache -r /tmp/requirements.txt
RUN mkdir /jupyterhub_users
RUN chown 1000:100 /jupyterhub_users