FROM python:3.9.0-alpine

RUN apk add --no-cache build-base postgresql-dev

WORKDIR /app
COPY ./requirements.txt .

RUN pip install --upgrade pip && \
    pip install gunicorn && \
    pip install -r requirements.txt

COPY . .

RUN ./manage.py migrate
CMD ["gunicorn", "--bind", ":8000", "--workers", "4", "feedback_service.wsgi:application"]