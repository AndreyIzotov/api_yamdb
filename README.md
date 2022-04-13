### Какую задачу решает:
Создает базу данных по различным видам и типам произведений
и на основе отзывов о них формирует оценки.


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:AndreyIzotov/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```


### Примеры:

Запрос на получение отзывов:
GET api/v1/titles/{title_id}/reviews/

Ответ:
```
[

{

    "count": 0,
    "next": "string",
    "previous": "string",
    "results": 

        []
    }

]
```

Запрос на получение комментариев к отзыву:
GET api/v1/titles/{title_id}/reviews/{review_id}/comments/

Ответ:
```
[

{

    "count": 0,
    "next": "string",
    "previous": "string",
    "results": 

        []
    }

]
```


### Наполнение базы

Для наполнения базы из .csv файлов имеется команда python manage.py import_csv
выполняющая импорт данных в следующем порядке:
1. users.csv
2. category.csv
3. genre.csv
4. titles.csv
5. review.csv
6. comments.csv
7. genre_title.csv

Образцы файлов расположены в папке /static.


После запуска проекта описание работы и остальные примеры доступны по адресу http://127.0.0.1:8000/redoc/
До запуска - в папке static файл redoc.html

Authors - Андрей Изотов, Станислав Сопов, Кирилл Ярков