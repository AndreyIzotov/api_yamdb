### Какую задачу решает:
Создает базу данных по различным видам и типам произведений
и на основе отзывов о ней формирует оценки.


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


После запуска проекта описание работы и остальные примеры доступны по адресу http://127.0.0.1:8000/redoc/
До запуска - в папке static файл redoc.html