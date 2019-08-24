from flask import Flask, request, jsonify
from dotenv import load_dotenv, find_dotenv
from app.db import jupyterhub, pg_pool, es
from app.api.users import users
from app.api.logs import logs


import psycopg2


def create_app():

    app = Flask(__name__)
    app.register_blueprint(users)
    app.register_blueprint(logs)

    @app.route("/")
    def hello():
        return "Hello World!"

    @app.route('/classes', methods=['GET', 'POST'])
    def show_classes(class_id):
        # if request.method == 'POST':
        #     return do_the_login()
        # else:
        #     return show_the_login_form()
        # con = pg_pool.getconn()
        # cursor = con.cursor()

        return class_id

    @app.route('/role', methods=['GET'])
    def show_access_role(class_id):
        # if request.method == 'POST':
        #     return do_the_login()
        # else:
        #     return show_the_login_form()
        log = request.get_json()
        username = log['username']

        conn = pg_pool.getconn()

        try:
            if conn:
                cur = conn.cursor()
                cur.execute(
                    'SELECT name, admin FROM jupyterhub.public.admin WHERE admin = true AND name = %s', (username))
                result = cur.fetchone()
                cur.close()

                if result:
                    return jsonify({
                        'role': 'admin'
                    })
            else:
                return jsonify({
                    'msg': 'Get pg connection error!',
                    'isError': True
                })
        finally:
            pg_pool.putconn(conn)

        return jsonify({
            'role': None
        })

    @app.route('/announcement', methods=['GET', 'POST'])
    def announcement():

        res_data = {}
        conn = pg_pool.getconn()
        try:
            if conn is None:
                return jsonify({
                    'msg': 'Get pg connection error!',
                    'isError': True
                })

            if request.method == 'POST':
                post_data = request.get_json()
                announcement_type = post_data['type']
                announcement_text = post_data['text']
                session_id = post_data['sessionId']

                # 判斷上傳公告種類
                if announcement_type == 'system' or announcement_type == 'normal':
                    try:
                        cur = conn.cursor()
                        # cur.execute('INSERT INTO viscode.public.system_announcements(type, content) VALUES (%s, %s) ON CONFLICT (type)', ('system'))
                        cur.execute(
                            'SELECT admin FROM oauth_access_tokens AS a, users AS b WHERE a.user_id = b.id AND a.session_id = %s AND b.admin = true', (session_id,))
                        result = cur.fetchone()

                        if result:
                            cur.execute('UPDATE system_announcements SET content = %s WHERE type = %s',
                                        (announcement_text, announcement_type))
                            updated_rows = cur.rowcount
                            conn.commit()
                            res_data = {
                                'msg': 'Updated announcement success!',
                                'isError': False
                            }

                        cur.close()
                    except (Exception, psycopg2.DatabaseError) as error:
                        print(error)
                        res_data = {
                            'msg': 'Updated announcement failed!',
                            'isError': True
                        }

                else:
                    res_data = {
                        'msg': 'Updated announcement failed!',
                        'isError': True
                    }

            elif request.method == 'GET':
                system_announcements = []
                normal_announcements = []

                cur = conn.cursor()
                cur.execute(
                    "SELECT title, content, shown FROM system_announcements WHERE type = %s", ('system',))
                system_results = cur.fetchall()
                cur.execute(
                    'SELECT title, content, shown FROM system_announcements WHERE type = %s', ('normal',))
                normal_results = cur.fetchall()
                cur.close()

                for row in system_results:
                    system_announcements.append({
                        'title': row[0],
                        'content': row[1],
                        'shown': row[2]
                    })

                for row in normal_results:
                    normal_announcements.append({
                        'title': row[0],
                        'content': row[1],
                        'shown': row[2]
                    })

                res_data = {
                    'systemAnnouncements': system_announcements,
                    'normalAnnouncements': normal_announcements
                }
        finally:
            pg_pool.putconn(conn)

        return jsonify(res_data)

    # @app.route('/classes/<class_id>', methods=['GET', 'PUT'])
    # def show_class(class_id):
    #     return class_id

    # @app.route('/classes/<class_id>/announcement', methods=['GET', 'PUT'])
    # def show_class_anouncement(class_id):
    #     return class_id

    # @app.route('/logs', methods=['POST'])
    # def add_log():
    #     log = request.get_json()
    #     log['timestamp'] = datetime.utcnow()

    #     try:
    #         jupyterhub.logs.insert(log.copy())
    #     except Exception as error:
    #         print("Error while connecting to MongoDB", error)

    #     try:
    #         res = es.index(index="viscode", doc_type='jupyter', body=log)
    #         # print(res['result'])
    #     except Exception as error:
    #         print("Error while connecting to Elasticsearch", error)

    #     return jsonify({
    #         'msg': 'success'
    #     })

    return app
