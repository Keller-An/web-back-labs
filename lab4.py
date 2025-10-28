from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)

    if x2 == 0:
        return render_template('lab4/div.html', error='Ошибка: на ноль делить нельзя!')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')


@lab4.route('/lab4/sum', methods=['POST'])
def sum_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sum.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')


@lab4.route('/lab4/sub', methods=['POST'])
def sub_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')


@lab4.route('/lab4/mul', methods=['POST'])
def mul_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/mul.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')


@lab4.route('/lab4/pow', methods=['POST'])
def pow_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Ошибка: 0⁰ не имеет смысла!')
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


tree_count = 0
max_trees = 10 

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, max_trees=max_trees)
    
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < max_trees:
        tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Иванов', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Боб Дилан', 'gender':'male'},
    {'login': 'maria', 'password': 'qwerty', 'name': 'Мария Петрова', 'gender':'female'},
    {'login': 'tom', 'password': 'admin', 'name': 'Том Харди', 'gender':'male'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    # если пользователь уже вошёл
    if request.method == 'GET':
        if 'login' in session:
            login_user = session['login']
            user = next((u for u in users if u['login'] == login_user), None)
            if user:
                return render_template('lab4/login.html', authorized=True, name=user['name'])
        return render_template('lab4/login.html', authorized=False, login='', error='')

    # получаем введённые данные
    login_input = request.form.get('login', '')
    password_input = request.form.get('password', '')

    if login_input.strip() == '':
        return render_template('lab4/login.html',
                               authorized=False,
                               error='Не введён логин',
                               login=login_input)

    if password_input.strip() == '':
        return render_template('lab4/login.html',
                               authorized=False,
                               error='Не введён пароль',
                               login=login_input)

    # проверка логина и пароля
    for user in users:
        if login_input == user['login'] and password_input == user['password']:
            session['login'] = login_input
            return redirect('/lab4/login')

    error = 'Неверный логин и/или пароль!'
    return render_template('lab4/login.html',
                           authorized=False,
                           error=error,
                           login=login_input)


@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')
    
    temp_str = request.form.get('temperature', '').strip()

    # если температура не задана
    if temp_str == '':
        return render_template('lab4/fridge.html', error='Ошибка: введите температуру!')
    
    try:
        temperature = float(temp_str)
    except ValueError:
        return render_template('lab4/fridge.html', error='Ошибка: введите корректное числовое значение температуры!')
    
    if temperature < -12:
        message = 'Не удалось установить температуру — слишком низкое значение!'
        snowflakes = 0
    elif temperature > -1:
        message = 'Не удалось установить температуру — слишком высокое значение!'
        snowflakes = 0
    elif -12 <= temperature <= -9:
        message = f'Установлена температура: {temperature}°C'
        snowflakes = 3
    elif -8 <= temperature <= -5:
        message = f'Установлена температура: {temperature}°C'
        snowflakes = 2
    else:
        message = f'Установлена температура: {temperature}°C'
        snowflakes = 1

    return render_template('lab4/fridge.html', message=message, snowflakes=snowflakes)


grains_price = {
    'ячмень': 12000,
    'овёс': 8500,
    'пшеница': 9000,
    'рожь': 15000
}

@lab4.route('/lab4/grain-order', methods=['GET', 'POST'])
def grain_order():
    if request.method == 'GET':
        return render_template('lab4/grain-order.html')
    
    grain = request.form.get('grain')
    weight_str = request.form.get('weight', '').strip()

    # проверка на пустой вес
    if weight_str == '':
        return render_template('lab4/grain-order.html', error='Ошибка: не указан вес!', grain=grain)

    try:
        weight = float(weight_str)
    except ValueError:
        return render_template('lab4/grain-order.html', error='Ошибка: вес должен быть числом!', grain=grain)

    if weight <= 0:
        return render_template('lab4/grain-order.html', error='Ошибка: вес должен быть больше 0!', grain=grain)

    if weight > 100:
        return render_template('lab4/grain-order.html', error='Ошибка: такого объёма зерна нет в наличии!', grain=grain)
    
    price_per_ton = grains_price.get(grain)
   
    total = weight * price_per_ton
    discount = 0
    discount_text = ''

    if weight > 10:
        discount = total * 0.1
        total -= discount
        discount_text = f'Применена скидка 10% за большой объём. Размер скидки: {discount:.2f} руб.'

    message = f'Заказ успешно сформирован. Вы заказали зерно: {grain}. Вес: {weight} т. Сумма к оплате: {total:.2f} руб.'
    return render_template('lab4/grain-order.html', message=message, discount_text=discount_text, grain=grain, weight=weight)



#Регистрация пользователя
@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html', error='', login='', name='')
    
    login_input = request.form.get('login', '').strip()
    name_input = request.form.get('name', '').strip()
    password_input = request.form.get('password', '').strip()
    confirm_input = request.form.get('confirm', '').strip()
    gender_input = request.form.get('gender', '').strip()

    # проверки
    if not login_input or not name_input or not password_input or not confirm_input:
        return render_template('lab4/register.html', error='Все поля обязательны!', login=login_input, name=name_input)
    if password_input != confirm_input:
        return render_template('lab4/register.html', error='Пароли не совпадают!', login=login_input, name=name_input)
    if any(u['login'] == login_input for u in users):
        return render_template('lab4/register.html', error='Такой логин уже существует!', login=login_input, name=name_input)

    # добавляем пользователя в массив
    users.append({
        'login': login_input,
        'password': password_input,
        'name': name_input,
        'gender': gender_input
    })

    # автоматически авторизуем
    session['login'] = login_input
    return redirect('/lab4/users')


#Просмотр списка пользователей
@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_user = session['login']
    current = next((u for u in users if u['login'] == current_user), None)
    return render_template('lab4/users.html', users=users, current_user=current_user, name=current['name'])
 

#Удаление пользователя
@lab4.route('/lab4/delete', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    login = session['login']
    global users
    users = [u for u in users if u['login'] != login]
    session.pop('login', None)
    return redirect('/lab4/login')


#Редактирование пользователя
@lab4.route('/lab4/edit', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    login = session['login']
    user = next((u for u in users if u['login'] == login), None)
    if not user:
        return redirect('/lab4/login')

    if request.method == 'GET':
        return render_template('lab4/edit.html', user=user, error='')

    new_login = request.form.get('login', '').strip()
    new_name = request.form.get('name', '').strip()
    new_password = request.form.get('password', '').strip()
    confirm = request.form.get('confirm', '').strip()

    # проверки
    if not new_login or not new_name:
        return render_template('lab4/edit.html', user=user, error='Имя и логин обязательны!')

    if new_password or confirm:
        if new_password != confirm:
            return render_template('lab4/edit.html', user=user, error='Пароли не совпадают!')
        else:
            user['password'] = new_password

    user['login'] = new_login
    user['name'] = new_name
    session['login'] = new_login

    return redirect('/lab4/users')