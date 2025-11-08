from flask import Blueprint, render_template, redirect, url_for, request
lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/')
def lab5_index():
    username = "Anonymous"
    return render_template('lab5/index.html', username=username)


@lab5.route('/lab5/login')
def lab5_login():
    return render_template('lab5/login.html')


@lab5.route('/lab5/register')
def lab5_register():
    return render_template('lab5/register.html')


@lab5.route('/lab5/list')
def lab5_list():
    return render_template('lab5/list.html')

    
@lab5.route('/lab5/create')
def lab5_create():
    return render_template('lab5/create.html')