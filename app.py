from flask import Flask, url_for, request
from datetime import datetime 
from lab1 import lab1
from lab2 import lab2 
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5 

app = Flask(__name__)

app.secret_key = 'секретно-секретный ключ'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
visit_log = []


@app.errorhandler(404)
def not_found(err):

    client_ip = request.remote_addr
    access_time = datetime.now()
    requested_url = request.url

    log_entry = f'[{access_time.strftime("%Y-%m-%d %H:%M:%S")}, пользователь {client_ip}] зашёл на адрес: {requested_url}'
    visit_log.append(log_entry)

    path = url_for("static", filename="lab1/окак.jpg")

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
              <li><a href="/lab2/">Лабораторная 2</a></li>
              <li><a href="/lab3/">Лабораторная 3</a></li>
              <li><a href="/lab4/">Лабораторная 4</a></li>
              <li><a href="/lab5/">Лабораторная 5</a></li>
        </nav>

        <footer>
            &copy; 2025 Махмадбекова Анастасия Эргашевна, ФБИ-32, 3 курс
        </footer>
    </body>
</html>
'''


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

