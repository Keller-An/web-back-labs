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
        
        data['fio'] = request.form.get('fio', '').strip()
        data['shelf'] = request.form.get('shelf', '')
        data['linen'] = request.form.get('linen')
        data['baggage'] = request.form.get('baggage')
        data['age'] = request.form.get('age', '')
        data['from_city'] = request.form.get('from_city', '').strip()
        data['to_city'] = request.form.get('to_city', '').strip()
        data['date'] = request.form.get('date', '')
        data['insurance'] = request.form.get('insurance')

        
        for field, value in data.items():
            if field not in ['linen', 'baggage', 'insurance'] and not value:
                errors[field] = 'Поле обязательно для заполнения!'

        
        if data['age']:
            try:
                age = int(data['age'])
                if not (1 <= age <= 120):
                    errors['age'] = 'Возраст должен быть от 1 до 120 лет!'
            except ValueError:
                errors['age'] = 'Возраст должен быть числом!'
        else:
            age = 0

        if not errors:
            if age < 18:
                base_price = 700
                ticket_type = 'Детский билет'
            else:
                base_price = 1000
                ticket_type = 'Взрослый билет'

            if data['shelf'] in ['нижняя', 'нижняя боковая']:
                base_price += 100

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


@lab3.route('/lab3/clear_settings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bgcolor')
    resp.delete_cookie('fontsize')
    resp.delete_cookie('fontstyle')
    return resp



@lab3.route('/lab3/cars')
def cars():
    cars = [
        {'name': 'Mercedes-Benz S-Class', 'price': 12500000, 'brand': 'Mercedes-Benz', 'color': 'черный', 'weight': 1950},
        {'name': 'BMW 7 Series', 'price': 11800000, 'brand': 'BMW', 'color': 'серый', 'weight': 1920},
        {'name': 'Audi A8', 'price': 11500000, 'brand': 'Audi', 'color': 'белый', 'weight': 1890},
        {'name': 'Lexus LS 500', 'price': 10800000, 'brand': 'Lexus', 'color': 'синий', 'weight': 1980},
        {'name': 'Porsche Panamera', 'price': 14500000, 'brand': 'Porsche', 'color': 'красный', 'weight': 1870},
        {'name': 'Jaguar XJ', 'price': 10200000, 'brand': 'Jaguar', 'color': 'черный', 'weight': 1820},
        {'name': 'Tesla Model S Plaid', 'price': 12500000, 'brand': 'Tesla', 'color': 'белый', 'weight': 2160},
        {'name': 'Bentley Continental GT', 'price': 23500000, 'brand': 'Bentley', 'color': 'темно-синий', 'weight': 2260},
        {'name': 'Rolls-Royce Ghost', 'price': 33000000, 'brand': 'Rolls-Royce', 'color': 'серебристый', 'weight': 2470},
        {'name': 'Aston Martin DB11', 'price': 26500000, 'brand': 'Aston Martin', 'color': 'темно-зеленый', 'weight': 1760},
        {'name': 'Ferrari Roma', 'price': 31000000, 'brand': 'Ferrari', 'color': 'красный', 'weight': 1570},
        {'name': 'Lamborghini Huracán', 'price': 34000000, 'brand': 'Lamborghini', 'color': 'желтый', 'weight': 1420},
        {'name': 'McLaren 720S', 'price': 35500000, 'brand': 'McLaren', 'color': 'оранжевый', 'weight': 1415},
        {'name': 'Maserati Quattroporte', 'price': 11700000, 'brand': 'Maserati', 'color': 'серый', 'weight': 1900},
        {'name': 'Porsche 911 Turbo S', 'price': 28500000, 'brand': 'Porsche', 'color': 'белый', 'weight': 1640},
        {'name': 'Bentley Flying Spur', 'price': 26500000, 'brand': 'Bentley', 'color': 'черный', 'weight': 2435},
        {'name': 'Rolls-Royce Cullinan', 'price': 43000000, 'brand': 'Rolls-Royce', 'color': 'темно-серый', 'weight': 2660},
        {'name': 'Ferrari SF90 Stradale', 'price': 48000000, 'brand': 'Ferrari', 'color': 'красный', 'weight': 1570},
        {'name': 'Lamborghini Aventador SVJ', 'price': 52000000, 'brand': 'Lamborghini', 'color': 'зеленый', 'weight': 1525},
        {'name': 'Bugatti Chiron', 'price': 230000000, 'brand': 'Bugatti', 'color': 'черно-синий', 'weight': 1995}
    ]

    min_price_cookie = request.cookies.get('min')
    max_price_cookie = request.cookies.get('max')
    min_user = request.args.get('min', min_price_cookie)
    max_user = request.args.get('max', max_price_cookie)

    if request.args.get('reset'):
        resp = make_response(redirect('/lab3/cars'))
        resp.delete_cookie('min')
        resp.delete_cookie('max')
        return resp

    # Фильтрация по цене
    filtered = cars
    try:
        if min_user or max_user:
            min_user = int(min_user) if min_user else min(car['price'] for car in cars)
            max_user = int(max_user) if max_user else max(car['price'] for car in cars)
            if min_user > max_user:
                min_user, max_user = max_user, min_user
            filtered = [c for c in cars if min_user <= c['price'] <= max_user]
    except ValueError:
        min_user = max_user = None

    resp = make_response(render_template(
        'lab3/cars.html',
        cars=filtered,
        total=len(filtered),
        min_price=min(car['price'] for car in cars),
        max_price=max(car['price'] for car in cars),
        min_user=min_user,
        max_user=max_user
    ))

    if min_user is not None:
        resp.set_cookie('min', str(min_user))
    if max_user is not None:
        resp.set_cookie('max', str(max_user))

    return resp