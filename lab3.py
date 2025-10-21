from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name') or 'Ноунейм'
    age = request.cookies.get('age') or 'Неизвестно'
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, age=age, name_color=name_color)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp = make_response('установка cookie', 200)
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    #Пусть кофе стоит 120 руб, черный чай - 80 руб, зеленый чай - 70 руб
    if drink == 'coffee':
        price = 120
    elif drink == 'black_tea':
        price = 80
    else:
        price = 70

    #Добавка молока удорожает напиток на 30 руб, а сахар на 10 руб
    if request.args.get('milk'):
        price += 30
    if request.args.get('sugar'):
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('lab3/success.html', price=price)



@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bgcolor = request.args.get('bgcolor')
    fontsize = request.args.get('fontsize')
    fontstyle = request.args.get('fontstyle')
    resp = make_response()

    if color or bgcolor or fontsize or fontstyle:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bgcolor:
            resp.set_cookie('bgcolor', bgcolor)
        if fontsize:
            resp.set_cookie('fontsize', fontsize)
        if fontstyle:
            resp.set_cookie('fontstyle', fontstyle)
        return resp

    color = request.cookies.get('color')
    bgcolor = request.cookies.get('bgcolor')
    fontsize = request.cookies.get('fontsize')
    fontstyle = request.cookies.get('fontstyle')

    resp = make_response(render_template('lab3/settings.html',
        color=color,
        bgcolor=bgcolor,
        fontsize=fontsize,
        fontstyle=fontstyle
    ))
    return resp


@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket():
    errors = {}
    data = {}

    if request.method == 'POST':
        # Получаем данные из формы
        data['fio'] = request.form.get('fio', '').strip()
        data['shelf'] = request.form.get('shelf', '')
        data['linen'] = request.form.get('linen')
        data['baggage'] = request.form.get('baggage')
        data['age'] = request.form.get('age', '')
        data['from_city'] = request.form.get('from_city', '').strip()
        data['to_city'] = request.form.get('to_city', '').strip()
        data['date'] = request.form.get('date', '')
        data['insurance'] = request.form.get('insurance')

        # Проверка заполненности
        for field, value in data.items():
            if field not in ['linen', 'baggage', 'insurance'] and not value:
                errors[field] = 'Поле обязательно для заполнения!'

        # Проверка возраста
        if data['age']:
            try:
                age = int(data['age'])
                if not (1 <= age <= 120):
                    errors['age'] = 'Возраст должен быть от 1 до 120 лет!'
            except ValueError:
                errors['age'] = 'Возраст должен быть числом!'
        else:
            age = 0

        # Если ошибок нет → считаем билет
        if not errors:
            # Расчёт цены
            if age < 18:
                base_price = 700
                ticket_type = 'Детский билет'
            else:
                base_price = 1000
                ticket_type = 'Взрослый билет'

            # Полка
            if data['shelf'] in ['нижняя', 'нижняя боковая']:
                base_price += 100

            # Опции
            if data['linen']:
                base_price += 75
            if data['baggage']:
                base_price += 250
            if data['insurance']:
                base_price += 150

            price = base_price

            return render_template(
                'lab3/ticket_result.html',
                data=data,
                ticket_type=ticket_type,
                price=price
            )

    return render_template('lab3/ticket_form.html', errors=errors, data=data)
