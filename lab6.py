import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app
from os import path
import sqlite3
from flask import Blueprint, render_template, request, session, url_for

lab6 = Blueprint('lab6', __name__)


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='anastasia_maxmadbekova_knowledge_base',
            user='anastasia_maxmadbekova_knowledge_base',
            password='weblabs'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()



@lab6.route('/lab6')
def main():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods = ['POST'])
def api():
    data = request.json
    id = data['id']
    if data['method'] == 'info':

        conn, cur = db_connect()
        cur.execute("SELECT * FROM offices ORDER BY number;")
        if current_app.config['DB_TYPE'] == 'postgres':
            offices = cur.fetchall() 
        else:
            offices = [dict(row) for row in cur.fetchall()]
        db_close(conn, cur)
    
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']

        conn, cur = db_connect()
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number=%s;", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number=?;", (office_number,))
        row = cur.fetchone()
        if row:
            row = dict(row)

        if not row:
            db_close(conn, cur)
            return {'jsonrpc':'2.0','error':{'code':5,'message':'Office not found'},'id':id}

        if row['tenant'] != '':
            db_close(conn, cur)
            return {'jsonrpc':'2.0','error':{'code':2,'message':'Already booked'},'id':id}

        # Бронируем
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE offices SET tenant=%s WHERE number=%s;", (login, office_number))
        else:
            cur.execute("UPDATE offices SET tenant=? WHERE number=?;", (login, office_number))
        db_close(conn, cur)

        return {'jsonrpc':'2.0','result':'success','id':id}

            
    if data['method'] == 'cancellation':
        office_number = data['params']

        conn, cur = db_connect()

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number=%s;", (office_number,))
        else:
             cur.execute("UPDATE offices SET tenant=? WHERE number=?;", ('', office_number))
        row = cur.fetchone()
        if row:
            row = dict(row)

        if not row:
            db_close(conn, cur)
            return {'jsonrpc':'2.0','error':{'code':5,'message':'Office not found'},'id':id}

        if row['tenant'] == '':
            db_close(conn, cur)
            return {'jsonrpc':'2.0','error':{'code':3,'message':'Office is not booked'},'id':id}

        if row['tenant'] != login:
            db_close(conn, cur)
            return {'jsonrpc':'2.0','error':{'code':4,'message':'Not your booking'},'id':id}

        # Отменяем бронь
        cur.execute("UPDATE offices SET tenant='' WHERE number=%s;", (office_number,))
        db_close(conn, cur)

        return {'jsonrpc':'2.0','result':'success','id':id}
