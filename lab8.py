from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from db import db
from db.models import users, articles

lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')
def main():
    return render_template('lab8/index.html', login = 'anonymous')


@lab8.route('/login')
def login():
    return ''

@lab8.route('/lab8/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or login_form.strip() == '':
        return render_template('lab8/register.html',
                               error = 'Имя пользователя не может быть пустым!', login_form = login_form)
    
    if not password_form or password_form.strip() == '':
        return render_template('lab8/register.html',
                               error = 'Пароль не может быть пустым!', login_form = login_form)

    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                               error = 'Такой пользователь уже существует', login_form = login_form)
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/lab8/')

@lab8.route('/list')
def list():
    return ''

@lab8.route('/create')
def create():
    return ''