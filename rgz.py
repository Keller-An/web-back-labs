from flask import Blueprint, request, render_template, redirect, session, current_app, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
import re
from datetime import datetime, time

rgz = Blueprint('rgz', __name__)



# База данных
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='anastasia_maxmadbekova_knowledge_base',
            user='anastasia_maxmadbekova_knowledge_base',
            password='weblabs'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.bd")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


# Валидация логина и пароля
def validate_latin_chars(text):
    if not text or not text.strip():
        return False, "Поле не может быть пустым"
    if not re.match(r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]*$', text):
        return False, "Можно использовать только латинские буквы, цифры и знаки препинания"
    return True, ""



# Главная страница - только фильмы
@rgz.route('/rgz/')
def main():
    conn, cur = db_connect()
    try:
        cur.execute("SELECT * FROM rgz_cinema_movies ORDER BY id DESC")
        movies_rows = cur.fetchall()
        movies = [dict(m) for m in movies_rows]
    finally:
        db_close(conn, cur)
    login = session.get('login')
    return render_template('rgz/rgz.html', movies=movies, login=login)


# Страница сеансов фильма
@rgz.route('/rgz/movie/<int:movie_id>')
def movie_sessions(movie_id):
    sessions = []  # Инициализация, чтобы точно существовала
    conn, cur = db_connect()
    try:
        # Получаем информацию о фильме
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM rgz_cinema_movies WHERE id=%s", (movie_id,))
        else:
            cur.execute("SELECT * FROM rgz_cinema_movies WHERE id=?", (movie_id,))
        movie_row = cur.fetchone()
        if not movie_row:
            return "Фильм не найден", 404
        
        movie = dict(movie_row)

        # Получаем сеансы фильма
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM rgz_cinema_sessions WHERE movie_id=%s ORDER BY date, time", (movie_id,))
        else:
            cur.execute("SELECT * FROM rgz_cinema_sessions WHERE movie_id=? ORDER BY date, time", (movie_id,))
        sessions_rows = cur.fetchall()
        sessions = [dict(s) for s in sessions_rows]

        # Добавляем поле is_past для каждого сеанса
        for s in sessions:
            sess_time = s['time']
            if isinstance(sess_time, time):
                time_str = sess_time.strftime("%H:%M:%S")
            else:
                time_str = str(sess_time)

            dt_format = "%Y-%m-%d %H:%M:%S" if len(time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
            session_datetime = datetime.strptime(f"{s['date']} {time_str}", dt_format)
            s['is_past'] = session_datetime < datetime.now()
            
    finally:
        db_close(conn, cur)
    
    login = session.get('login')
    return render_template('rgz/movie.html', movie=movie, sessions=sessions, login=login)




# Страница бронирования мест
@rgz.route('/rgz/booking/<int:session_id>')
def booking(session_id):
    conn, cur = db_connect()
    try:
        # Получаем информацию о сеансе и фильме
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT s.*, m.title as movie_title, m.duration 
                FROM rgz_cinema_sessions s
                JOIN rgz_cinema_movies m ON s.movie_id = m.id
                WHERE s.id=%s
            """, (session_id,))
        else:
            cur.execute("""
                SELECT s.*, m.title as movie_title, m.duration 
                FROM rgz_cinema_sessions s
                JOIN rgz_cinema_movies m ON s.movie_id = m.id
                WHERE s.id=?
            """, (session_id,))
        session_info = cur.fetchone()
        if session_info:
            session_info = dict(session_info)  # конвертируем в словарь

        
        if not session_info:
            return "Сеанс не найден", 404
        
        # Проверяем, прошел ли сеанс
        # Для функции booking
        sess_time = session_info['time']
        if isinstance(sess_time, time):
            time_str = sess_time.strftime("%H:%M:%S")  # или "%H:%M", если без секунд
        else:
            time_str = str(sess_time)

        # Теперь проверка формата
        if len(time_str.split(':')) == 2:
            dt_format = "%Y-%m-%d %H:%M"
        else:
            dt_format = "%Y-%m-%d %H:%M:%S"

        session_datetime = datetime.strptime(f"{session_info['date']} {time_str}", dt_format)
        is_past = session_datetime < datetime.now()
        
        # Получаем информацию о занятых местах
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT b.id, b.seat_number, u.full_name 
                FROM rgz_cinema_bookings b
                JOIN rgz_cinema_users u ON b.user_id = u.id
                WHERE b.session_id=%s
            """, (session_id,))
        else:
            cur.execute("""
                SELECT b.id, b.seat_number, u.full_name 
                FROM rgz_cinema_bookings b
                JOIN rgz_cinema_users u ON b.user_id = u.id
                WHERE b.session_id=?
            """, (session_id,))
        booked_seats = cur.fetchall()
        
        # Получаем места текущего пользователя
        user_seats = []
        if session.get('user_id'):
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT seat_number FROM rgz_cinema_bookings WHERE session_id=%s AND user_id=%s", 
                          (session_id, session['user_id']))
            else:
                cur.execute("SELECT seat_number FROM rgz_cinema_bookings WHERE session_id=? AND user_id=?", 
                          (session_id, session['user_id']))
            user_seats = [s['seat_number'] for s in cur.fetchall()]
            
    finally:
        db_close(conn, cur)
    
    login = session.get('login')
    return render_template('rgz/booking.html', 
                         session=session_info, 
                         booked_seats=booked_seats,
                         user_seats=user_seats,
                         is_past=is_past,
                         login=login)



# Регистрация пользователя
@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')

    full_name = request.form.get('full_name')
    login = request.form.get('login')
    password = request.form.get('password')

    # Валидация
    is_valid_login, login_error = validate_latin_chars(login)
    is_valid_password, password_error = validate_latin_chars(password)
    if not is_valid_login:
        return render_template('rgz/register.html', error=login_error)
    if not is_valid_password:
        return render_template('rgz/register.html', error=password_error)
    if not (full_name and login and password):
        return render_template('rgz/register.html', error='Заполните все поля')

    conn, cur = db_connect()
    try:
        # Проверка уникальности логина
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM rgz_cinema_users WHERE login=%s", (login,))
        else:
            cur.execute("SELECT * FROM rgz_cinema_users WHERE login=?", (login,))
        if cur.fetchone():
            return render_template('rgz/register.html', error='Пользователь уже существует')

        password_hash = generate_password_hash(password)

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO rgz_cinema_users (full_name, login, password_hash, is_admin) VALUES (%s, %s, %s, %s)",
                        (full_name, login, password_hash, False))
        else:
            cur.execute("INSERT INTO rgz_cinema_users (full_name, login, password_hash, is_admin) VALUES (?, ?, ?, ?)",
                        (full_name, login, password_hash, 0))
    finally:
        db_close(conn, cur)

    return render_template('rgz/register_success.html', login=login)


# Логин пользователя
@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')

    login_input = request.form.get('login')
    password = request.form.get('password')

    is_valid_login, login_error = validate_latin_chars(login_input)
    is_valid_password, password_error = validate_latin_chars(password)
    if not is_valid_login:
        return render_template('rgz/login.html', error=login_error)
    if not is_valid_password:
        return render_template('rgz/login.html', error=password_error)

    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM rgz_cinema_users WHERE login=%s", (login_input,))
        else:
            cur.execute("SELECT * FROM rgz_cinema_users WHERE login=?", (login_input,))
        user = cur.fetchone()
    finally:
        db_close(conn, cur)

    if not user or not check_password_hash(user['password_hash'], password):
        return render_template('rgz/login.html', error='Неверный логин или пароль')

    session['login'] = user['login']
    session['user_id'] = user['id']
    session['is_admin'] = user.get('is_admin', False)

    return redirect('/rgz/')


# Выход из аккаунта
@rgz.route('/rgz/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return redirect('/rgz/login')



# JSON-RPC ответ
def json_rpc_response(result=None, error=None, request_id=None):
    response = {"jsonrpc": "2.0", "id": request_id}
    if error:
        response["error"] = error
    else:
        response["result"] = result
    return jsonify(response)


# Получить сеансы фильма
def get_sessions(params, request_id):
    movie_id = params.get('movie_id')
    if not movie_id:
        return json_rpc_response(None, {"code": -32602, "message": "Invalid params"}, request_id)
    conn, cur = db_connect()
    try:
        cur.execute("SELECT * FROM rgz_cinema_sessions WHERE movie_id=? ORDER BY date, time" if current_app.config['DB_TYPE']=='sqlite' else
                    "SELECT * FROM rgz_cinema_sessions WHERE movie_id=%s ORDER BY date, time", (movie_id,))
        sessions = [dict(s) for s in cur.fetchall()]
        # Получаем занятые места и кто их занял
        booked = {}
        for session_item in sessions:
            session_id = session_item['id']
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""SELECT b.seat_number, u.full_name FROM rgz_cinema_bookings b
                               JOIN rgz_cinema_users u ON b.user_id = u.id
                               WHERE b.session_id=%s""", (session_id,))
            else:
                cur.execute("""SELECT b.seat_number, u.full_name FROM rgz_cinema_bookings b
                               JOIN rgz_cinema_users u ON b.user_id = u.id
                               WHERE b.session_id=?""", (session_id,))
            booked[session_id] = [{"seat": b["seat_number"], "user": b["full_name"]} for b in cur.fetchall()]
    finally:
        db_close(conn, cur)
    return json_rpc_response({"sessions": sessions, "booked": booked}, None, request_id)


# Бронирование / снятие брони
def toggle_booking(params, request_id):
    user_id = session.get('user_id')
    if not user_id:
        return json_rpc_response(None, {"code": 1, "message": "Необходима авторизация"}, request_id)

    session_id = params.get('session_id')
    seat_numbers = params.get('seat_numbers')  # <-- массив мест
    action_type = params.get('action_type', 'book')

    if not session_id or not seat_numbers:
        return json_rpc_response(None, {"code": -32602, "message": "Invalid params"}, request_id)

    # если пришло одно место, приводим к списку
    if isinstance(seat_numbers, int):
        seat_numbers = [seat_numbers]

    conn, cur = db_connect()
    try:
        # Получаем дату/время сеанса
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT date, time, price FROM rgz_cinema_sessions WHERE id=%s", (session_id,))
        else:
            cur.execute("SELECT date, time, price FROM rgz_cinema_sessions WHERE id=?", (session_id,))
        session_row = cur.fetchone()
        if not session_row:
            return json_rpc_response(None, {"code": 4, "message": "Сеанс не найден"}, request_id)

        sess_date = session_row['date']
        sess_time = session_row['time']
        price = session_row['price']

        if isinstance(sess_time, time):
            time_str = sess_time.strftime("%H:%M:%S")
        else:
            time_str = str(sess_time)
        dt_format = "%Y-%m-%d %H:%M:%S" if len(time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
        session_dt = datetime.strptime(f"{sess_date} {time_str}", dt_format)

        if session_dt < datetime.now():
            return json_rpc_response(None, {"code": 5, "message": "Нельзя изменять прошедший сеанс"}, request_id)

        # перебираем все места
        results = []
        for seat_number in seat_numbers:
            # Проверяем, занято ли место
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM rgz_cinema_bookings WHERE session_id=%s AND seat_number=%s", (session_id, seat_number))
            else:
                cur.execute("SELECT * FROM rgz_cinema_bookings WHERE session_id=? AND seat_number=?", (session_id, seat_number))
            booking = cur.fetchone()

            action = ""
            if action_type == "book":
                if booking:
                    if booking['user_id'] == user_id:
                        action = "already_booked"
                    else:
                        return json_rpc_response(None, {"code": 2, "message": f"Место {seat_number} уже занято"}, request_id)
                else:
                    # проверка лимита 5 мест
                    if current_app.config['DB_TYPE'] == 'postgres':
                        cur.execute("SELECT COUNT(*) FROM rgz_cinema_bookings WHERE session_id=%s AND user_id=%s", (session_id, user_id))
                        current_count = cur.fetchone()['count']
                    else:
                        cur.execute("SELECT COUNT(*) FROM rgz_cinema_bookings WHERE session_id=? AND user_id=?", (session_id, user_id))
                        current_count = cur.fetchone()[0]
                    if current_count >= 5:
                        return json_rpc_response(None, {"code": 3, "message": "Нельзя выбрать больше 5 мест"}, request_id)

                    # бронирование
                    if current_app.config['DB_TYPE'] == 'postgres':
                        cur.execute("INSERT INTO rgz_cinema_bookings (user_id, session_id, seat_number) VALUES (%s, %s, %s)", (user_id, session_id, seat_number))
                    else:
                        cur.execute("INSERT INTO rgz_cinema_bookings (user_id, session_id, seat_number) VALUES (?, ?, ?)", (user_id, session_id, seat_number))
                    action = "booked"

            elif action_type == "cancel":
                if booking and booking['user_id'] == user_id:
                    if current_app.config['DB_TYPE'] == 'postgres':
                        cur.execute("DELETE FROM rgz_cinema_bookings WHERE session_id=%s AND seat_number=%s AND user_id=%s", (session_id, seat_number, user_id))
                    else:
                        cur.execute("DELETE FROM rgz_cinema_bookings WHERE session_id=? AND seat_number=? AND user_id=?", (session_id, seat_number, user_id))
                    action = "cancelled"
                else:
                    action = "not_booked"

            results.append({"seat": seat_number, "action": action})

        # обновленный список мест пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT seat_number FROM rgz_cinema_bookings WHERE session_id=%s AND user_id=%s", (session_id, user_id))
        else:
            cur.execute("SELECT seat_number FROM rgz_cinema_bookings WHERE session_id=? AND user_id=?", (session_id, user_id))
        current_user_seats = [r['seat_number'] for r in cur.fetchall()]
        total_price = price * len(current_user_seats)

    finally:
        db_close(conn, cur)

    return json_rpc_response({"success": True, "results": results, "seats": current_user_seats, "total_price": total_price}, None, request_id)



# Получить выбранные места и цену
def get_selected_seats(params, request_id):
    user_id = session.get('user_id')
    if not user_id:
        return json_rpc_response(None, {"code": 1, "message": "Необходима авторизация"}, request_id)
    session_id = params.get('session_id')
    if not session_id:
        return json_rpc_response(None, {"code": -32602, "message": "Invalid params"}, request_id)

    conn, cur = db_connect()
    try:
        # Получаем места пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT seat_number FROM rgz_cinema_bookings WHERE session_id=%s AND user_id=%s", 
                       (session_id, user_id))
        else:
            cur.execute("SELECT seat_number FROM rgz_cinema_bookings WHERE session_id=? AND user_id=?", 
                       (session_id, user_id))
        seats = [s['seat_number'] for s in cur.fetchall()]
        
        # Получаем цену за билет (отдельный запрос)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT price FROM rgz_cinema_sessions WHERE id=%s", (session_id,))
        else:
            cur.execute("SELECT price FROM rgz_cinema_sessions WHERE id=?", (session_id,))
        price_row = cur.fetchone()
        price_per_seat = price_row['price'] if price_row else 0
        total_price = price_per_seat * len(seats)
    finally:
        db_close(conn, cur)

    return json_rpc_response({"seats": seats, "total_price": total_price}, None, request_id)


# Удаление аккаунта
def delete_account(params, request_id):
    user_id = session.get('user_id')
    if not user_id:
        return json_rpc_response(None, {"code": 1, "message": "Необходима авторизация"}, request_id)
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM rgz_cinema_users WHERE id=%s", (user_id,))
            cur.execute("DELETE FROM rgz_cinema_bookings WHERE user_id=%s", (user_id,))
        else:
            cur.execute("DELETE FROM rgz_cinema_users WHERE id=?", (user_id,))
            cur.execute("DELETE FROM rgz_cinema_bookings WHERE user_id=?", (user_id,))
    finally:
        db_close(conn, cur)
        session.clear()
    return json_rpc_response({"success": True}, None, request_id)



# Администраторские функции
def admin_add_session(params, request_id):
    if not session.get('is_admin'):
        return json_rpc_response(None, {"code": 1, "message": "Требуется администратор"}, request_id)
    movie_id = params.get('movie_id')
    date = params.get('date')
    time = params.get('time')
    price = params.get('price', 0)
    if not movie_id or not date or not time or price <= 0:
        return json_rpc_response(None, {"code": -32602, "message": "Неверные параметры"}, request_id)
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO rgz_cinema_sessions (movie_id, date, time, price) VALUES (%s, %s, %s, %s)", (movie_id, date, time, price))
        else:
            cur.execute("INSERT INTO rgz_cinema_sessions (movie_id, date, time, price) VALUES (?, ?, ?, ?)", (movie_id, date, time, price))
    finally:
        db_close(conn, cur)
    return json_rpc_response({"success": True}, None, request_id)


def admin_delete_session(params, request_id):
    if not session.get('is_admin'):
        return json_rpc_response(None, {"code": 1, "message": "Требуется администратор"}, request_id)
    session_id = params.get('session_id')
    if not session_id:
        return json_rpc_response(None, {"code": -32602, "message": "Invalid params"}, request_id)
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM rgz_cinema_sessions WHERE id=%s", (session_id,))
            cur.execute("DELETE FROM rgz_cinema_bookings WHERE session_id=%s", (session_id,))
        else:
            cur.execute("DELETE FROM rgz_cinema_sessions WHERE id=?", (session_id,))
            cur.execute("DELETE FROM rgz_cinema_bookings WHERE session_id=?", (session_id,))
    finally:
        db_close(conn, cur)
    return json_rpc_response({"success": True}, None, request_id)


#  снятие брони администратором
# Исправьте функцию admin_cancel_booking:
def admin_cancel_booking(params, request_id):
    if not session.get('is_admin'):
        return json_rpc_response(None, {"code": 1, "message": "Требуется администратор"}, request_id)
    
    booking_id = params.get('booking_id')
    if not booking_id:
        return json_rpc_response(None, {"code": -32602, "message": "Invalid params"}, request_id)
    
    conn, cur = db_connect()
    try:
        # Получаем информацию о бронировании и сеансе
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT b.*, s.date, s.time 
                FROM rgz_cinema_bookings b
                JOIN rgz_cinema_sessions s ON b.session_id = s.id
                WHERE b.id=%s
            """, (booking_id,))
        else:
            cur.execute("""
                SELECT b.*, s.date, s.time 
                FROM rgz_cinema_bookings b
                JOIN rgz_cinema_sessions s ON b.session_id = s.id
                WHERE b.id=?
            """, (booking_id,))
        
        booking = cur.fetchone()
        
        if not booking:
            return json_rpc_response(None, {"code": 6, "message": "Бронирование не найдено"}, request_id)
        
        # Проверяем, не прошел ли сеанс
        sess_date = booking['date']
        sess_time = booking['time']
        
        if isinstance(sess_time, time):
            time_str = sess_time.strftime("%H:%M:%S")
        else:
            time_str = str(sess_time)
        
        dt_format = "%Y-%m-%d %H:%M:%S" if len(time_str.split(':')) == 3 else "%Y-%m-%d %H:%M"
        session_dt = datetime.strptime(f"{sess_date} {time_str}", dt_format)
        
        if session_dt < datetime.now():
            return json_rpc_response(None, {"code": 5, "message": "Нельзя отменять бронирования прошедших сеансов"}, request_id)
        
        # Удаляем бронирование
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM rgz_cinema_bookings WHERE id=%s", (booking_id,))
        else:
            cur.execute("DELETE FROM rgz_cinema_bookings WHERE id=?", (booking_id,))
        
        deleted_count = cur.rowcount
            
    finally:
        db_close(conn, cur)
    
    return json_rpc_response({
        "success": True, 
        "message": "Бронирование отменено",
        "deleted_count": deleted_count
    }, None, request_id)


#функции создания фильмов (админ)
def admin_add_movie(params, request_id):
    if not session.get('is_admin'):
        return json_rpc_response(None, {"code": 1, "message": "Требуется администратор"}, request_id)
    
    title = params.get('title')
    description = params.get('description', '')
    duration = params.get('duration', 0)
    
    if not title or duration <= 0:
        return json_rpc_response(None, {"code": -32602, "message": "Неверные параметры"}, request_id)
    
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO rgz_cinema_movies (title, description, duration) VALUES (%s, %s, %s)",
                       (title, description, duration))
        else:
            cur.execute("INSERT INTO rgz_cinema_movies (title, description, duration) VALUES (?, ?, ?)",
                       (title, description, duration))
    finally:
        db_close(conn, cur)
    
    return json_rpc_response({"success": True}, None, request_id)



# Просмотр всех бронирований (админ)
def admin_view_all_bookings(params, request_id):
    if not session.get('is_admin'):
        return json_rpc_response(None, {"code": 1, "message": "Требуется администратор"}, request_id)
    
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT b.id AS booking_id, u.full_name AS user_name, m.title AS movie_title, 
                       s.date, s.time, b.seat_number, s.price
                FROM rgz_cinema_bookings b
                JOIN rgz_cinema_users u ON b.user_id = u.id
                JOIN rgz_cinema_sessions s ON b.session_id = s.id
                JOIN rgz_cinema_movies m ON s.movie_id = m.id
                ORDER BY s.date, s.time, b.seat_number
            """)
        else:
            cur.execute("""
                SELECT b.id AS booking_id, u.full_name AS user_name, m.title AS movie_title, 
                       s.date, s.time, b.seat_number, s.price
                FROM rgz_cinema_bookings b
                JOIN rgz_cinema_users u ON b.user_id = u.id
                JOIN rgz_cinema_sessions s ON b.session_id = s.id
                JOIN rgz_cinema_movies m ON s.movie_id = m.id
                ORDER BY s.date, s.time, b.seat_number
            """)
        bookings = [dict(b) for b in cur.fetchall()]
    finally:
        db_close(conn, cur)
    
    return json_rpc_response({"bookings": bookings}, None, request_id)


# Отмена всех бронирований на сеансе (админ)
def admin_cancel_all_bookings(params, request_id):
    if not session.get('is_admin'):
        return json_rpc_response(None, {"code": 1, "message": "Требуется администратор"}, request_id)
    
    session_id = params.get('session_id')
    if not session_id:
        return json_rpc_response(None, {"code": -32602, "message": "Invalid params"}, request_id)
    
    conn, cur = db_connect()
    try:
        # Проверяем, существует ли сеанс
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM rgz_cinema_sessions WHERE id=%s", (session_id,))
        else:
            cur.execute("SELECT * FROM rgz_cinema_sessions WHERE id=?", (session_id,))
        
        if not cur.fetchone():
            return json_rpc_response(None, {"code": 4, "message": "Сеанс не найден"}, request_id)
        
        # Удаляем все бронирования для этого сеанса
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM rgz_cinema_bookings WHERE session_id=%s", (session_id,))
            deleted_count = cur.rowcount
        else:
            cur.execute("DELETE FROM rgz_cinema_bookings WHERE session_id=?", (session_id,))
            deleted_count = cur.rowcount
            
    finally:
        db_close(conn, cur)
    
    return json_rpc_response({
        "success": True, 
        "message": f"Удалено {deleted_count} бронирований",
        "deleted_count": deleted_count
    }, None, request_id)



# JSON-RPC API
@rgz.route('/rgz/api', methods=['POST'])
def api():
    data = request.get_json()
    if not data or 'jsonrpc' not in data or data['jsonrpc'] != '2.0' or 'method' not in data:
        return jsonify({"jsonrpc":"2.0","error":{"code":-32600,"message":"Invalid Request"},"id":data.get('id') if data else None})

    method = data.get('method')
    params = data.get('params', {})
    request_id = data.get('id')

    if method == 'get_sessions':
        return get_sessions(params, request_id)
    elif method == 'book_seat' or method == 'toggle_booking':
        return toggle_booking(params, request_id)
    elif method == 'get_selected_seats':
        return get_selected_seats(params, request_id)
    elif method == 'delete_account':
        return delete_account(params, request_id)
    elif method == 'admin_add_session':
        return admin_add_session(params, request_id)
    elif method == 'admin_delete_session':
        return admin_delete_session(params, request_id)
    elif method == 'admin_add_movie':
        return admin_add_movie(params, request_id)
    elif method == 'admin_view_all_bookings':
        return admin_view_all_bookings(params, request_id)
    elif method == 'admin_cancel_booking':
        return admin_cancel_booking(params, request_id)
    elif method == 'admin_cancel_all_bookings':
        return admin_cancel_all_bookings(params, request_id)
    else:
        return jsonify({"jsonrpc":"2.0","error":{"code":-32601,"message":"Method not found"},"id":request_id})
