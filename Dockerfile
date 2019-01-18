FROM python:3.7-alpine
LABEL maintainer="https://github.com/sdbenezra"

ENV PYTHONUNBUFFERED 1

EXPOSE 8080

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
     gcc libc-dev linux-headers python-dev postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
USER user
RUN python manage.py wait_for_db && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
