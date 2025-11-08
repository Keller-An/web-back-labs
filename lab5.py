from flask import Blueprint, render_template, redirect, request, session, current_app, url_for,  flash
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path 
lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab():
    return render_template('lab5/index.html', login=session.get('login'))


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'anastasia_maxmadbekova_knowledge_base',
            user = 'anastasia_maxmadbekova_knowledge_base',
            password = 'weblabs'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
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


@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error="Заполните поля!")
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', 
                               error='Логин и/или пароль неверны!')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', 
                               error='Логин и/или пароль неверны!')
    
    session['login'] = login
    db_close(conn, cur)
    return render_template('lab5/success_login.html', login=login)


@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    flash("Вы вышли из системы", "success")
    return redirect(url_for('lab5.lab'))



@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля!')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login, ))

    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                               error="Такой пользователь уже существует!")
    
    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s);", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
    conn.commit() 
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)

    
@lab5.route('/lab5/create', methods = ['POST', 'GET'])
def create():
    login=session.get('login')
    if not login:
        return redirect('lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html', login=login)

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()

    if not title or not article_text:
        return render_template(
            'lab5/create_article.html',
            login=login,
            edit=False,
            article={'title': title, 'article_text': article_text},
            error="Тема и текст статьи не могут быть пустыми!"
        )
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/create_article.html', error='Пользователь не найден!')

    user_id = user['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO articles (user_id, title, article_text) VALUES (%s, %s, %s);",
            (user_id, title, article_text)
        )
    else:
        cur.execute(
            "INSERT INTO articles (user_id, title, article_text) VALUES (?, ?, ?);",
            (user_id, title, article_text)
        )

    db_close(conn, cur)
    return redirect('/lab5/')


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login = %s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login = ?;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/articles.html', articles=[], error="Пользователь не найден")

    user_id = user['id']

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE user_id = %s;", (user_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE user_id = ?;", (user_id,))
    articles = cur.fetchall()

    db_close(conn, cur)
    
    if not articles:
        message = "У вас пока нет ни одной статьи"
    else:
        message = None

    return render_template('lab5/articles.html', articles=articles, message=message)


@lab5.route('/lab5/edit/<int:article_id>', methods=['GET','POST'])
def edit(article_id):
    login_input = session.get('login')
    if not login_input:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
    article = cur.fetchone()

    if request.method == 'POST':
        title = request.form.get('title').strip()
        text = request.form.get('article_text').strip()
        if not title or not text:
            flash("Тема и текст статьи не могут быть пустыми!", "error")
            return redirect(url_for('lab5.edit', article_id=article_id))
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, text, article_id))
        else:
            cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, text, article_id))
        db_close(conn, cur)
        flash("Статья обновлена", "success")
        return redirect(url_for('lab5.list'))

    db_close(conn, cur)
    return render_template('lab5/create_article.html', article=article, login=login_input, edit=True)


@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete(article_id):
    login_input = session.get('login')
    if not login_input:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))
    db_close(conn, cur)
    flash("Статья удалена", "success")
    return redirect(url_for('lab5.list'))