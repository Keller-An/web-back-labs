from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from sqlalchemy import or_, func
from flask_login import login_user, login_required, current_user, logout_user
from db.models import users, articles

lab8 = Blueprint('lab8', __name__)


@lab8.route('/lab8/')
def main():
    if current_user.is_authenticated:
        return render_template('lab8/index.html', login=current_user.login)
    return render_template('lab8/index.html')


@lab8.route('/lab8/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember_me')

    if not login_form or login_form.strip() == '':
        return render_template('lab8/login.html',
                               error = 'Логин не может быть пустым', login_form = login_form)
    
    if not password_form or password_form.strip() == '':
        return render_template('lab8/login.html',
                               error = 'Пароль не может быть пустым', login_form = login_form)

    user = users.query.filter_by(login = login_form).first() 

    if user:
        if check_password_hash(user.password, password_form):
            remember = bool(remember_me)
            login_user(user, remember = remember)
            return redirect('/lab8/')

    return render_template('/lab8/login.html',
                           error = 'Ошибка входа: логин и/или пароль неверны')   


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

    login_user(new_user, remember = False)

    return redirect('/lab8/')



@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = bool(request.form.get('is_public'))
    is_favorite = bool(request.form.get('is_favorite'))

    if not title or not article_text:
        return render_template('lab8/create.html', 
                               error='Все поля обязательны!',
                               title=title, 
                               article_text=article_text,
                               is_public=is_public,
                               is_favorite=is_favorite)

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_public=is_public,
        is_favorite=is_favorite,
        likes=0
    )
    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/articles/')


@lab8.route('/lab8/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return "Доступ запрещен", 403

    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_public = bool(request.form.get('is_public'))
        is_favorite = bool(request.form.get('is_favorite'))

        if not title or not article_text:
            return render_template('lab8/edit.html', error='Все поля обязательны!', article=article)

        article.title = title
        article.article_text = article_text
        article.is_public = is_public
        article.is_favorite = is_favorite

        db.session.commit()
        return redirect('/lab8/articles/')

    return render_template('lab8/edit.html', article=article)


@lab8.route('/lab8/delete/<int:article_id>/', methods=['POST'])
@login_required
def delete(article_id):
    article = articles.query.get_or_404(article_id)

    if article.login_id != current_user.id:
        return "Доступ запрещен", 403

    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/articles/')



@lab8.route('/lab8/articles/')
def articles_list():
    # Проверяем, есть ли параметр поиска
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        # Если есть поисковый запрос, используем функцию поиска
        return search_articles()
    
    # Иначе показываем все статьи как раньше
    if current_user.is_authenticated:
        user_articles = articles.query.filter(
            (articles.login_id == current_user.id) | (articles.is_public == True)
        ).all()
    else:
        user_articles = articles.query.filter_by(is_public=True).all()

    return render_template('lab8/articles.html', articles=user_articles)



@lab8.route('/lab8/articles/search/', methods=['GET'])
def search_articles():
    search_query = request.args.get('q', '').strip()

    from sqlalchemy import or_, func

    if current_user.is_authenticated:
        base_filter = or_(
            articles.login_id == current_user.id,
            articles.is_public == True
        )
    else:
        base_filter = articles.is_public == True

    if search_query:
        q = search_query.lower()
        user_articles = articles.query.filter(
            base_filter,
            or_(
                func.lower(articles.title).contains(q),
                func.lower(articles.article_text).contains(q)
            )
        ).all()
    else:
        user_articles = articles.query.filter(base_filter).all()

    return render_template(
        'lab8/articles.html',
        articles=user_articles,
        search_query=search_query
    )

