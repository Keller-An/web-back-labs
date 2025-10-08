from flask import Blueprint, redirect, url_for
from lab1 import lab1
lab1= Blueprint('lab1', __name__)


lab1 = Flask(__name__)
lab1.register_blueprint(lab1)


@lab1.route("/lab1")
def lab():
    return '''
<!doctype html>
<html>
    <head>
    <title>Лабораторная работа 1</title>
    <style>
        body {
            font-family: times new roman;
            background-color: #faeeff;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #007539;
            text-algin: center;
        }
        p {
            font-size: 20px;
        }
    </style>
    </head>

    <body>
        <h1>Лабораторная 1</h1>
        <p>
            Flask — фреймворк для создания веб-приложений на языке
            программирования Python, использующий набор инструментов
            Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
            называемых микрофреймворков — минималистичных каркасов
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <a href="/">Вернуться на главную</a>

        <h2>Список роутов</h2>
        <ul>
            <li><a href="/">/</a></li>
            <li><a href="/index">/index</a></li>
            <li><a href="/lab1">/lab1</a></li>
            <li><a href="/lab1/web">/lab1/web</a></li>
            <li><a href="/lab1/author">Автор</a></li>
            <li><a href="/lab1/image">Изображение</a></li>
            <li><a href="/lab1/counter">Счетчик</a></li>
            <li><a href="/lab1/counter/clear">Очиста счетчика</a></li>
            <li><a href="/lab1/info">Информация об авторе</a></li>
            <li><a href="/lab1/created">Создание</a></li>
            <li><a href="/401">401</a></li>
            <li><a href="/402">402</a></li>
            <li><a href="/403">403</a></li>
            <li><a href="/404">404</a></li>
            <li><a href="/405">405</a></li>
            <li><a href="/418">418</a></li>
            <li><a href="/500test">/500test</a></li>
        </ul>
    </body>
</html>
'''


@lab1.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервис на flask</h1>
               <a href="/author">author</a>
           </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
        }


@lab1.route("/lab1/author")
def author():
    name = "Махмадбекова Анастасия Эргашевна"
    group = "ФБИ-32"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
           <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/">web</a>
            </body>
        </html>"""


@lab1.route("/lab1/image")
def image():
    path = url_for("static", filename="image.jpg")
    css_path = url_for("static", filename="lab1.css")
    return'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Том Харди</h1>
        <h3>I wanna da-, I wanna dance in the lights<br>
        I wanna ro-, I wanna rock your body</h3>
        <img src="''' + path + '''">
    </body>
</html>
''', 200, {
    'Content-Language': 'en',
    'X-Content-Created': '23.09.2025',
    'X-Author': 'Anastasia Mahmadbekova',
}


count = 0
@lab1.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + str(url) + '''<br>
        Ваш IP адрес: ''' + str(client_ip) + '''<br>
        <a href="counter/clear">Сбросить счётчик</a>
    </body>
</html>
'''


@lab1.route("/lab1/counter/clear")
def counter_clear():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        <h1>Счётчик сброшен</h1>
        <a href="/lab1/counter">Вернуться обратно к счётчику<a/>
    </body>
</html>
'''

@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@lab1.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201 
