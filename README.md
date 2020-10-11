# feedback-service

## [Доска Kanban](https://github.com/5000factorial/feedback-service/projects/1)

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
3. Установить зависимости
```
pip3 install -r requirements.txt
```
4. Применить миграции
```
python3 manage.py migrate
```
5. Запустить
```
python3 manage.py runserver
```
