FROM python:3.10 as base

WORKDIR /url_shortener

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5001

FROM base as dev

ENTRYPOINT gunicorn -b 0.0.0.0:${SHORTENER_APP_PORT} -w ${SHORTENER_APP_GEVENT_WORKERS} wsgi_app:app -k gevent



