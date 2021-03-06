from pymongo import MongoClient
from elasticsearch import Elasticsearch
from psycopg2 import pool
from dotenv import load_dotenv, find_dotenv
import psycopg2
import os

load_dotenv(find_dotenv())

es_hosts = os.getenv('ELASTICSEARCH_HOSTS', '127.0.0.1')
es_host_list = es_hosts.split(',')

mongodb_host = os.getenv('MONGODB_HOST', '127.0.0.1')
mongodb_port = os.getenv('MONGODB_PORT', '27017')
mongodb_user = os.getenv('MONGODB_USER', 'user')
mongodb_password = os.getenv('MONGODB_PASSWORD', 'password')
use_mongodb = True if os.getenv('USE_MONGODB', 'FALSE') == '1' else False

pg_host = os.getenv('POSTGRES_HOST', '127.0.0.1')
pg_port = os.getenv('POSTGRES_PORT', 5432)
pg_user = os.getenv('POSTGRES_USER', 'postgres')
pg_password = os.getenv('POSTGRES_PASSWORD', '')
pg_database = os.getenv('POSTGRES_DATABASE', 'jupyterhub')

#print(es_host_list)

# MongoDB
if use_mongodb:
    #client = MongoClient(maxPoolSize=30, connect=False)
    client = MongoClient('mongodb://{}:{}@{}:{}/'.format(mongodb_user, mongodb_password, mongodb_host, mongodb_port))
    try:
        test = client.server_info()
        print('MongoDB connection created successfully')
        jupyterhub = client.VISCODE #DB name
    except:
        print('Failed to create MongoDB connection')
        jupyterhub = None
else:
    jupyterhub = None
    print('To available MongoDB, set USE_MONGODB=1')
    
# Elasticsearch
es = Elasticsearch(
    es_host_list,
    maxsize=5,
    # sniff_on_start=True,
    sniff_on_connection_fail=True,
    sniffer_timeout=60
)
# es = Elasticsearch()

if es:
    print('Elasticsearch connection created successfully')

# Postgres
pg_pool = pool.ThreadedConnectionPool(
    1, 3, user=pg_user, password=pg_password, host=pg_host,
    port=pg_port, database=pg_database)
if pg_pool:
    print('Postgres connection pool created successfully')

def get_pg_pool():
    return pg_pool

def get_es():
    return es

def get_jupyterhub():
    return jupyterhub
