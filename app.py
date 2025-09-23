from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "Такой страницы не существует :(", 404

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

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервис на flask</h1>
               <a href="/author">author</a>
           </body>
        <html>""", 200, {
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
                <a href="/web">web</a>
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
'''

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
        <a href="/counter">Вернуться обратно к счётчику<a/>
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