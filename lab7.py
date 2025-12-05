from flask import Blueprint, render_template, request, abort, jsonify
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


films = [
    {
        "title": "The Lord of the Rings: The Return of the King",
        "title_ru": "Властелин колец: Возвращение короля",
        "year": 2003,
        "description": "Повелитель сил тьмы Саурон направляет свою бесчисленную армию \
            под стены Минас-Тирита, крепости Последней Надежды. Он предвкушает близкую победу, \
            но именно это мешает ему заметить две крохотные фигурки — хоббитов, приближающихся \
            к Роковой Горе, где им предстоит уничтожить Кольцо Всевластья."
    },
    {
        "title": "Forrest Gump",
        "title_ru": "Форрест Гамп",
        "year": 1994,
        "description": "Сидя на автобусной остановке, Форрест Гамп — не очень умный, \
            но добрый и открытый парень — рассказывает случайным встречным \
            историю своей необыкновенной жизни. С самого малолетства парень \
            страдал от заболевания ног, соседские мальчишки дразнили его, \
            но в один прекрасный день Форрест открыл в себе невероятные \
            способности к бегу. Подруга детства Дженни всегда его \
            поддерживала и защищала, но вскоре дороги их разошлись."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": "Сотрудник страховой компании страдает хронической \
        бессонницей и отчаянно пытается вырваться из мучительно скучной жизни. \
        Однажды в очередной командировке он встречает некоего \
        Тайлера Дёрдена — харизматического торговца мылом с извращенной философией. \
        Тайлер уверен, что самосовершенствование — удел слабых, \
        а единственное, ради чего стоит жить, — саморазрушение."
    },
    {
        "title": "Knockin' on Heaven's Door",
        "title_ru": "Достучаться до небес",
        "year": 1997,
        "description": "Волею судеб две абсолютные противоположности, \
        тихоня Руди и разгильдяй Мартин, оказываются в одной больничной палате. \
        Узнав неутешительные прогнозы, друзья решают использовать последние \
        дни на полную катушку — угнать машину с деньгами, \
        напиться текилы, и, конечно, увидеть море."
    }  
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return jsonify(films[id])


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_films(id):
    if id < 0 or id >= len(films):
        abort(404)
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    film = request.get_json()

    errors, validated_film = validate_film(film)
    if errors:
        return jsonify(errors), 400

    films[id] = validated_film
    return jsonify(validated_film)


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    errors, validated_film = validate_film(film)
    if errors:
        return jsonify(errors), 400

    films.append(validated_film)
    return jsonify({"id": len(films) - 1}), 201


def validate_film(film):
    errors = {}
    current_year = datetime.now().year

    title = film.get('title', '').strip()
    title_ru = film.get('title_ru', '').strip()

    # если нет ни одного названия — ошибка
    if not title and not title_ru:
        errors['title'] = 'Необходимо указать хотя бы одно название: оригинальное или русское'

    # если есть русское название, но оригинальное пустое — присваиваем
    if not title and title_ru:
        title = title_ru

    # проверка года
    try:
        year_int = int(film.get('year', 0))
        if year_int < 1895:
            errors['year'] = f'Год фильма не может быть раньше 1895'
        elif year_int > current_year:
            errors['year'] = f'Год фильма не может быть больше {current_year}'
    except (ValueError, TypeError):
        errors['year'] = 'Год фильма должен быть числом'

    # проверка описания
    description = film.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание обязательно для заполнения'
    elif len(description) > 2000:
        errors['description'] = f'Описание не должно превышать 2000 символов (сейчас: {len(description)})'

    validated_film = {
        'title': title,
        'title_ru': title_ru,
        'year': year_int if 'year_int' in locals() else 0,
        'description': description
    }

    return errors, validated_film