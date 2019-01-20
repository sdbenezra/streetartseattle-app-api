FROM python:3.7-alpine
LABEL maintainer="https://github.com/sdbenezra"

ENV PYTHONUNBUFFERED 1

EXPOSE 8080

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev uwsgi-python3
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

ENV UWSGI_WSGI_FILE=app/wsgi.py UWSGI_HTTP=:8080 UWSGI_MASTER=1 UWSGI_WORKERS=2 UWSGI_THREADS=8 UWSGI_UID=1000 UWSGI_GID=2000 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy
# ENTRYPOINT ["tail", "-f", "/dev/null"]
CMD ["uwsgi", "--http-auto-chunked", "--http-keepalive"]
