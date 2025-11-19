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
    real_name = request.form.get('real_name')

    if not (login and password and real_name):
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
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);", (login, password_hash, real_name))
    else:
        cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", (login, password_hash, real_name))
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
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'

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
            "INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) VALUES (%s, %s, %s, %s, %s);",
            (user_id, title, article_text, is_favorite, is_public)
        )
    else:
        cur.execute(
             "INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) VALUES (?, ?, ?, ?, ?);",
            (user_id, title, article_text, is_favorite, is_public)
        )

    db_close(conn, cur)
    return redirect('/lab5/')


@lab5.route('/lab5/list')
def list():
    login = session.get('login')
    conn, cur = db_connect()

    user_id = None
    own_count = 0

    if login:
        # получить id пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
        else:
            cur.execute("SELECT id FROM users WHERE login=?;", (login,))
        user = cur.fetchone()
        user_id = user['id']

        # считаем количество СВОИХ статей
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT COUNT(*) AS cnt FROM articles WHERE user_id=%s;", (user_id,))
        else:
            cur.execute("SELECT COUNT(*) AS cnt FROM articles WHERE user_id=?;", (user_id,))

        row = cur.fetchone()
        own_count = row['cnt'] if row else 0

        # получаем свои + публичные
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT a.*, u.login, u.real_name
                FROM articles a
                JOIN users u ON a.user_id = u.id
                WHERE a.user_id = %s OR a.is_public = true
                ORDER BY a.is_favorite DESC, a.id;
            """, (user_id,))
        else:
            cur.execute("""
                SELECT a.*, u.login, u.real_name
                FROM articles a
                JOIN users u ON a.user_id = u.id
                WHERE a.user_id = ? OR a.is_public = 1
                ORDER BY a.is_favorite DESC, a.id;
            """, (user_id,))
    else:
        # не авторизован — только публичные
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT a.*, u.login, u.real_name
                FROM articles a
                JOIN users u ON a.user_id = u.id
                WHERE a.is_public = true
                ORDER BY a.is_favorite DESC, a.id;
            """)
        else:
            cur.execute("""
                SELECT a.*, u.login, u.real_name
                FROM articles a
                JOIN users u ON a.user_id = u.id
                WHERE a.is_public = 1
                ORDER BY a.is_favorite DESC, a.id;
            """)

    articles = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/articles.html', articles=articles, login=login, own_count=own_count, user_id=user_id)




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


@lab5.route('/lab5/users')
def users():
    conn, cur = db_connect()
    cur.execute("SELECT login, real_name FROM users;")
    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/users.html', users=users)


@lab5.route('/lab5/profile', methods = ['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))
    
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login = %s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login = ?;", (login, ))
    user = cur.fetchone()

    if request.method == 'POST':
        real_name = request.form.get('real_name').strip()
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm')

        if not real_name:
            db_close(conn, cur)
            return render_template('lab5/profile.html', user=user, error="Имя не может быть пустым!")

        if new_password:
            if new_password != confirm_password:
                db_close(conn, cur)
                return render_template('lab5/profile.html', user=user, error="Пароли не совпадают!")
            password_hash = generate_password_hash(new_password)
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE users SET real_name=%s, password=%s WHERE login=%s;", (real_name, password_hash, login))
            else:
                cur.execute("UPDATE users SET real_name=?, password=? WHERE login=?;", (real_name, password_hash, login))
        else:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE users SET real_name=%s WHERE login=%s;", (real_name, login))
            else:
                cur.execute("UPDATE users SET real_name=? WHERE login=?;", (real_name, login))

        db_close(conn, cur)
        return render_template('lab5/profile.html', user=user, message="Изменения сохранены!")

    db_close(conn, cur)
    return render_template('lab5/profile.html', user=user)


@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()
    cur.execute("""
        SELECT a.title, a.article_text, u.login, u.real_name
        FROM articles a
        JOIN users u ON a.user_id = u.id
        WHERE a.is_public = true
        ORDER BY a.is_favorite DESC, a.id;
    """)
    articles = cur.fetchall()
    db_close(conn, cur)
    return render_template('lab5/public_articles.html', articles=articles)
