import random
from flask import Blueprint, abort, redirect, render_template, render_template_string, request 
lab2= Blueprint('lab2', __name__)




@lab2.route('/lab2/a/')
def a ():
    return 'со слэшем'


@lab2.route('/lab2/a')
def a2 ():
    return 'без слэша'


flower_list = ['Роза', 'Ромашка', 'Одуванчик', 'Незабудка']
flower_prices = {
    'Роза': 300,
    'Ромашка': 250,
    'Одуванчик': 280,
    'Незабудка': 200
}



@lab2.route('/lab2/all_flowers')
def all_flowers():
    total_price = sum(flower_prices.get(f, 300) for f in flower_list)
    return render_template('flowers.html',
                           flowers=flower_list,
                           flower_prices=flower_prices,
                           total_price=total_price)



@lab2.route('/lab2/add_flower/', methods=['POST'])
def add_flower_form():
    name = request.form.get('flower_name', '').strip()
    if name:
        flower_list.append(name)
        flower_prices[name] = random.randint(100, 400)
    return redirect('/lab2/all_flowers')


@lab2.route('/lab2/del_flower/<int:flower_id>')
def delete_flower(flower_id):
    if flower_id < 0 or flower_id >= len(flower_list):
        abort(404)
    flower_list.pop(flower_id)
    return redirect('/lab2/all_flowers')


@lab2.route('/lab2/del_all_flowers')
def delete_all_flowers():
    flower_list.clear()
    return redirect('/lab2/all_flowers')


@lab2.route('/lab2/flowers/rewrite')
def rewrite_flowers():
    flower_list.clear()
    flower_list.extend(['Роза', 'Ромашка', 'Одуванчик', 'Незабудка'])
    return redirect('/lab2/all_flowers')


@lab2.route('/lab2/example')
def example():
    name, lab_number, group, course = 'Махмадбекова Анастасия', 2, 'ФБИ-32', 3
    fruits = [
        {'name': 'яблоки', 'price':100},
        {'name': 'груши', 'price':120},
        {'name': 'апельсины', 'price':80},
        {'name': 'мандарины', 'price':95},
        {'name': 'манго', 'price':321},
        ]
    return render_template('example.html',
                           name=name, lab_number=lab_number, group=group,
                           course=course, fruits=fruits)


@lab2.route('/lab2/')
def lab2_index():
    return render_template('lab2.html') 


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)


# Перенаправление по умолчанию на /lab2/calc/1/1
@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


# Перенаправление, если задан только один параметр
@lab2.route('/lab2/calc/<int:a>')
def calc_one(a):
    return redirect(f'/lab2/calc/{a}/1')


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc_two(a, b):
    html = f'''
    <!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Расчёт с параметрами</title>
        </head>
        <body>
            <h2>Расчёт с параметрами:</h2>
            <p>{a} + {b} = {a + b}</p>
            <p>{a} - {b} = {a - b}</p>
            <p>{a} × {b} = {a * b}</p>
            <p>{a} / {b} = {a / b if b != 0 else "деление на ноль"}</p>
            <p>{a}<sup>{b}</sup> = {a ** b}</p>
        </body>
    </html>
    '''
    return render_template_string(html)


@lab2.route('/lab2/books')
def books():
    book_list = [
        {"author": "Донна Тартт", "title": "Щегол", "genre": "Современная проза", "pages": 864},
        {"author": "Стивен Кинг", "title": "Сияние", "genre": "Ужасы", "pages": 672},
        {"author": "Фредрик Бакман", "title": "Вторая жизнь Уве", "genre": "Драма", "pages": 416},
        {"author": "Эрих Мария Ремарк", "title": "Три товарища", "genre": "Роман", "pages": 480},
        {"author": "Евгений Замятин", "title": "Мы", "genre": "Антиутопия", "pages": 320},
        {"author": "Джордж Оруэлл", "title": "Скотный двор", "genre": "Сатира, антиутопия", "pages": 192},
        {"author": "Дж. Р. Р. Толкин", "title": "Хоббит, или Туда и обратно", "genre": "Фэнтези", "pages": 208},
        {"author": "Дж. К. Роулинг", "title": "Гарри Поттер и узник Азкабана", "genre": "Фэнтези", "pages": 528},
        {"author": "Фёдор Достоевский", "title": "Идиот", "genre": "Роман", "pages": 736},
        {"author": "Габриэль Гарсиа Маркес", "title": "Сто лет одиночества", "genre": "Магический реализм", "pages": 512}
    ]
    return render_template('books.html', books=book_list)



items = [
    {"name": "Котик 1", "desc": "Милый рыжий котик", "img": "1.jpg"},
    {"name": "Котик 2", "desc": "Кот возмущается", "img": "2.jpg"},
    {"name": "Котик 3", "desc": "Крутой кот", "img": "3.jpg"},
    {"name": "Котик 4", "desc": "Кот не понял", "img": "4.jpg"},
    {"name": "Котик 5", "desc": "Кот в недоумении", "img": "5.jpg"},
    {"name": "Котик 6", "desc": "Кот смотрит на вас вопросительно", "img": "6.jpg"},
    {"name": "Котик 7", "desc": "Йомайо", "img": "7.jpg"},
    {"name": "Котик 8", "desc": "У кота рот смешной...", "img": "8.jpg"},
    {"name": "Котик 9", "desc": "Нарисованный кот", "img": "9.jpg"},
    {"name": "Котик 10", "desc": "Кот типо работает", "img": "10.jpg"},
    {"name": "Котик 11", "desc": "Кот промок...", "img": "11.jpg"},
    {"name": "Котик 12", "desc": "Чилловый кот", "img": "12.jpg"},
    {"name": "Котик 13", "desc": "Сейлим в карты играет", "img": "13.jpg"},
    {"name": "Котик 14", "desc": "Сейлим в гламурной одежде", "img": "14.jpg"},
    {"name": "Котик 15", "desc": "Кот с наушниками", "img": "15.jpg"},
    {"name": "Котик 16", "desc": "Три крутых кота", "img": "16.jpg"},
    {"name": "Котик 17", "desc": "Кот дарит вам розу", "img": "17.jpg"},
    {"name": "Котик 18", "desc": "Кот влюблен в вас", "img": "18.jpg"},
    {"name": "Котик 19", "desc": "Три не менее крутых кота", "img": "19.jpg"},
    {"name": "Котик 20", "desc": "Черный кот", "img": "20.jpg"},
]


@lab2.route("/lab2/cats")
def show_cats():
    html = '''
    <!doctype html>
    <html>
        <head>
            <title>Список котиков</title>
            <style>
                body { font-family: Arial; background: #f9f9f9; text-align: center; }
                .item { display: inline-block; margin: 20px; border: 1px solid #ccc; border-radius: 10px; padding: 10px; background: #fff; width: 200px; }
                img { width: 180px; height: 180px; object-fit: cover; border-radius: 10px; }
                h3 { margin: 10px 0 5px; color: #333; }
                p { margin: 0; color: #666; }
            </style>
        </head>
        <body>
            <h1>Список котиков</h1>
            {% for item in items %}
                <div class="item">
                    <img src="{{ url_for('static', filename=item.img) }}" alt="{{ item.name }}">
                    <h3>{{ item.name }}</h3>
                    <p>{{ item.desc }}</p>
                </div>
            {% endfor %}
        </body>
    </html>
    '''
    return render_template_string(html, items=items) 