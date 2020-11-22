# feedback-service

## [Доска Kanban](https://github.com/5000factorial/feedback-service/projects/1)
## [Сервер](https://feedback-service-spbu.herokuapp.com)

## Установка
0. Убедиться что есть python3
1. Создать [virtual environment](https://docs.python.org/3/library/venv.html)
```
python3 -m venv venv
```
2. Активировать virtual environment
```
. venv/bin/activate
```
4. Установить зависимости
```
pip3 install -r requirements.txt
```
5. Применить миграции
```
python3 manage.py migrate
```
6. Создать администратора
```
python3 manage.py createsuperuser
```
7. Запустить
```
python3 manage.py runserver
```

Админка будет доступна по адресу localhost:8000/admin/
