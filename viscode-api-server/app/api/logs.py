from flask import Blueprint, jsonify, request
from app.db import get_pg_pool, get_jupyterhub, get_es
from datetime import datetime, timedelta
from bson.json_util import dumps
import psycopg2

logs = Blueprint('logs', __name__,
                 template_folder='templates')

es = get_es()
jupyterhub = get_jupyterhub()


@logs.route('/logs', methods=['POST'])
def add_log():
    log = request.get_json()
    log['timestamp'] = datetime.utcnow()

    try:
        if jupyterhub:
            jupyterhub.logs.insert(log.copy())
    except Exception as error:
        print("Error while connecting to MongoDB", error)

    try:
        res = es.index(index="viscode", doc_type='jupyter', body=log)
        # print(res['result'])
    except Exception as error:
        print("Error while connecting to Elasticsearch", error)

    return jsonify({
        'msg': 'success'
    })


@logs.route('/logs', methods=['get'])
def get_log():
    limit = request.args.get('limit', default=10, type=int)
    page = request.args.get('page', default=1, type=int)
    minute = request.args.get('minute', default=15, type=int)
    event_type = request.args.get('type', type=str)

    now = datetime.utcnow()
    query_time = now - timedelta(minutes=minute)
    query_filter = {
        'timestamp': {
            '$lte': now,
            '$gt': query_time
        }
    }
    result = []

    if event_type:
        query_filter.update({
            'event': event_type
        })

    try:
        if jupyterhub:
            logs = jupyterhub.logs.find(query_filter).limit(limit).skip(limit*(page-1))
            for log in logs:
                result.append(log)
    except Exception as error:
        print("Error while connecting to MongoDB", error)

    return dumps({'logs': result})
