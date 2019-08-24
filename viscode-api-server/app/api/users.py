from flask import Blueprint, jsonify, request
from app.db import get_pg_pool
import psycopg2

users = Blueprint('users', __name__,
                        template_folder='templates')

pg_pool = get_pg_pool()

@users.route('/users', methods=['POST'])
def handle_users():
    res_data = {}
    conn = pg_pool.getconn()

    try:
        if conn is None:
            return jsonify({
                'msg': 'Database connection error!',
                'isError': True
            })

        if request.method == 'POST':
            post_data = request.get_json()
            account = post_data['account']
            password = post_data['password']
            session_id = post_data['sessionId']

            try:
                cur = conn.cursor()
                # cur.execute('INSERT INTO viscode.public.system_announcements(type, content) VALUES (%s, %s) ON CONFLICT (type)', ('system'))
                cur.execute(
                    'SELECT admin FROM oauth_access_tokens AS a, users AS b WHERE a.user_id = b.id AND a.session_id = %s AND b.admin = true', (session_id,))
                is_admin = cur.fetchone()

                if is_admin:
                    cur.execute('SELECT * FROM user_passwords WHERE name = %s', (account,))
                    is_existed = cur.fetchone()

                    if is_existed is None:
                        cur.execute('INSERT INTO user_passwords(name, password) VALUES (%s, %s)',
                                    (account, password))
                        conn.commit()
                        count = cur.rowcount
                        res_data = {
                            'msg': 'Add account success.',
                            'isError': False,
                            'count': count
                        }
                    else:
                        res_data = {
                            'msg': 'Account exsited',
                            'isError': True,
                        }
                else:
                    res_data = {
                        'msg': 'Permission denied',
                        'isError': True,
                    }

                cur.close()
            except (Exception, psycopg2.Error) as error:
                print(error)
                res_data = {
                    'msg': error,
                    'isError': True
                }
    finally:         
        pg_pool.putconn(conn)

    return jsonify(res_data)

@users.route('/users/<string:account>', methods=['PATCH'])
def patch_user(account):
    res_data = {}
    conn = pg_pool.getconn()

    try:
        if conn is None:
            return jsonify({
                'msg': 'Database connection error!',
                'isError': True
            })
        
        post_data = request.get_json()
        password = post_data['password']
        session_id = post_data['sessionId']

        cur = conn.cursor()
        # cur.execute('INSERT INTO viscode.public.system_announcements(type, content) VALUES (%s, %s) ON CONFLICT (type)', ('system'))
        cur.execute(
            'SELECT admin FROM oauth_access_tokens AS a, users AS b WHERE a.user_id = b.id AND a.session_id = %s AND b.admin = true', (session_id,))
        is_admin = cur.fetchone()

        if is_admin:
            cur.execute('SELECT * FROM user_passwords WHERE name = %s', (account,))
            is_existed = cur.fetchone()

            if is_existed:
                cur.execute('UPDATE user_passwords SET password = %s WHERE name = %s',
                            (password, account))
                conn.commit()
                count = cur.rowcount
                res_data = {
                    'msg': 'Update account success.',
                    'isError': False,
                    'count': count
                }
            else:
                res_data = {
                    'msg': 'Account do not exsited',
                    'isError': True,
                }
        else:
            res_data = {
                'msg': 'Permission denied',
                'isError': True,
            }

        cur.close()
    except (Exception, psycopg2.Error) as error:
        print(error)
        res_data = {
            'msg': error,
            'isError': True
        }
    finally:    
        pg_pool.putconn(conn)

    return jsonify(res_data)