from flask import Blueprint, render_template, request, abort, jsonify

lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')
def main():
    return render_template('lab8/index.html', login = 'anonymous')


@lab8.route('/login')
def login():
    return ''

@lab8.route('/register')
def register():
    return ''


@lab8.route('/list')
def list():
    return ''

@lab8.route('/create')
def create():
    return ''