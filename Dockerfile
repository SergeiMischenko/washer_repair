FROM python:3.12.3-slim

SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /app

RUN mkdir /app/static && mkdir /app/media

COPY . .

RUN pip install -r requirements.txt

RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "-b", "0.0.0.0:8000", "washer_repair.wsgi:application"]