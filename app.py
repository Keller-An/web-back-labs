from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_faund(err):
    return "Такой страницы не существует :(", 404

@app.route("/")
@app.route("/web")
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

@app.route("/author")
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

@app.route("/image")
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
@app.route('/counter')
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
    </body>
</html>
'''

@app.route("/info")
def info():
    return redirect("/author")

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