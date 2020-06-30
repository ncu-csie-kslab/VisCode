FROM jupyterhub/jupyterhub:1.2
RUN mkdir /jupyterhub_users
RUN chown 1000:100 /jupyterhub_users
RUN apt-get update \
 && apt-get install -yq --no-install-recommends \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache -r /tmp/requirements.txt
