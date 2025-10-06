from flask import Flask, url_for, request, redirect, abort, render_template
import datetime


app = Flask(__name__)
visit_log = []

@app.errorhandler(404)
def not_found(err):

    client_ip = request.remote_addr
    access_time = datetime.datetime.now()
    requested_url = request.url

    log_entry = f'[{access_time.strftime("%Y-%m-%d %H:%M:%S")}, пользователь {client_ip}] зашёл на адрес: {requested_url}'
    visit_log.append(log_entry)

    path = url_for("static", filename="окак.jpg")

    journal_html = ''
    for entry in reversed(visit_log[-10:]):
        journal_html += f'<div class="log-entry">{entry}</div>'

    return f'''
<!doctype html>
<html>
    <head>
    <title>404 - Страница не найдена</title>
        <style>
            body {{
                background-color: #c7c7ff;
                font-family: Jazz LET, fantasy;
                text-align: center;
                padding: 50px;
                color: #563fb0;
            }}
            h1 {{
                font-size: 64px;
                margin: 0;
                color: #43328a;
            }}
            p {{
                font-size: 24px;
            }}
            .user-info, .error-journal {{
                text-align: left;
                display: inline-block;
                margin-top: 20px;
                background: #e0e0ff;
                padding: 15px;
                border-radius: 8px;
            }}
            a {{
                display: inline-block;
                margin-top: 20px;
                background: #2e8b57;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
            }}
            a:hover {{
                background: #246b46;
            }}
            img {{
                max-width: 400px;
                margin-top: 30px;
            }}
            
        </style>
    </head>
    <body>
        <h1>404</h1>
        <p>Поздравляю, вы сломали браузер</p>
        <p>Попробуйте вернуться на главную, хотя мало чем поможет</p>
        <div class="user-info">
            <h3>Информация о запросе:</h3>
            <p><strong>IP-адрес:</strong> {client_ip}</p>
            <p><strong>Дата и время:</strong> {access_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Запрошенный URL:</strong> {requested_url}</p>
            <a href="/" class="error-home-button">На главную</a>
        </div>
         
        <div>
            <img src="{path}" alt="404" class="error-image">
        </div>

        <div class="error-journal">
            <h3>Журнал последних посещений:</h3>
            {journal_html if journal_html else '<p>Пока нет записей в журнале</p>'}
        </div>
''', 404

@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                margin: 0;
                padding: 0;
            }
            header {
                background-color: #2e8b57;
                color: white;
                padding: 20px;
                text-align: center;
            }
            nav {
                margin: 20px;
            }
            nav li {
                margin: 10px 0;
            }
            nav a {
                color: green;
                font-weight: bold;
            }
            footer {
                background-color: #333333;
                color: white;
                padding: 10px;
                text-align: center;
                margin-top: auto;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>

        <nav>
            <li><a href="/lab1">Лабораторная 1</a></li>
        </nav>

        <footer>
            &copy; 2025 Махмадбекова Анастасия Эргашевна, ФБИ-32, 3 курс
        </footer>
    </body>
</html>
'''
@app.route("/lab1")
def lab1():
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

@app.route("/lab1/web")
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

@app.route("/lab1/author")
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

@app.route("/lab1/image")
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
@app.route('/lab1/counter')
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

@app.route("/lab1/counter/clear")
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

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
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

@app.route("/400")
def error400():
    return '''
<!doctype html>
<html>
    <head><title>400 Bad Request</title></head>
    <body>
        <h1>400 Bad Request</h1>
        <p>Сервер не может или не будет обрабатывать запрос из-за чего-то, 
        что воспринимается как ошибка клиента (например, неправильный синтаксис, 
        формат или маршрутизация запроса).</p>
    </body>
</html>
''', 400

@app.route("/401")
def error401():
    return '''
<!doctype html>
<html>
    <head><title>401 Unauthorized</title></head>
    <body>
    <h1>401 Unauthorized</h1>
    <p>для доступа к запрашиваемому ресурсу требуется аутентификация.</p>
''',401

@app.route("/402")
def error402():
    return '''
<!doctype html>
<html>
    <head><title>402 Payment Required</title></head>
    <body>
    <h1>402 Payment Required</h1>
    <p>Этот код предусмотрен для платных пользовательских сервисов</p>
''',402

@app.route("/403")
def error403():
    return '''
<!doctype html>
<html>
    <head><title>403 Forbidden</title></head>
    <body>
    <h1>403 Forbidden</h1>
    <p>У вас нет прав для доступа к этому ресурсу</p>
''',403

@app.route("/405")
def error405():
    return '''
<!doctype html>
<html>
    <head><title>405 Method Not Allowed</title></head>
    <body>
    <h1>405 Method Not Allowed</h1>
    <p>Метод запроса известен серверу, но не поддерживается целевым ресурсом.</p>
''',405

@app.route("/418")
def error418():
    return '''
<!doctype html>
<html>
    <head><title>418 I'm a teapot</title></head>
    <body>
    <h1>418 I'm a teapot</h1>
    <p>Я чайник, я не могу заварить кофе, но могу сделать чай :)</p>
''', 418

@app.route("/500test")
def error500():
    x = 1 / 0
    return str(x)

@app.errorhandler(500)
def debug_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <style>
            body {
                text-align: center;
                padding: 50px;
            }
            h1 {
                font-size: 60px;
                margin: 0;
                color: #a00020;
            }
            p {
                font-size: 20px;
            }
            a {
                display: inline-block;
                margin-top: 20px;
                text-decoration: none;
                background: #b00020;
                color: white;
                padding: 10px 20px;
                border-radius: 8px;
                transition: background 0.3s;
            }
        </style>
        <title>500 - Внутренняя ошибка сервера</title>
    </head>
    <body>
        <h1>500</h1>
        <p>На сервере произошла внутренняя ошибка</p>
        <p>Попробуйте позже или вернитесь на главную страницу.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 500

@app.route('/lab2/a/')
def a ():
    return 'со слэшем'

@app.route('/lab2/a')
def a2 ():
    return 'без слэша'

flower_list = ['роза', 'тюльпан', 'пион', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок=" + flower_list[flower_id]
    
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name = 'Махмадбекова Анастасия'
    lab_number = 2
    group = 'ФБИ-32'
    course = 3
    return render_template(
        'example.html', 
        name=name, 
        lab_number=lab_number,
        group=group,
        course=course
    )
