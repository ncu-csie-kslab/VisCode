FROM tiangolo/uwsgi-nginx-flask:python3.7

# ENV POSTGRES_HOST postgres
# ENV POSTGRES_HOST postgres
# ENV ELASTICSEARCH_HOST es01,es02

# COPY ./app /app
COPY ./app /app/app
COPY ./requirements.txt /app/

COPY ./uwsgi.ini /app
# COPY ./main.py /app/app

RUN pip install -r /app/requirements.txt