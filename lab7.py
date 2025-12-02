from flask import Blueprint, render_template, request, abort

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
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return films[id]


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
    if film['description'] == '':
        return {'description': 'Заполните описание!'}, 400
    films[id] = film
    return films[id]


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if not film.get('description', '').strip():
        return{'description': 'Заполните описание'}, 400
    films.append(film)
    return{"id": len(films) - 1}