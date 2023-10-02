# base image
FROM python:3.11

# enviironment variables
ENV HOME=/
ENV APP_HOME=/django/movies_admin_panel/app
ENV GROUP=django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE 'config.settings'

WORKDIR $APP_HOME

RUN apt-get update && apt-get install -y gettext && apt install -y ncat
RUN python -m pip install --upgrade pip

RUN apt-get update && \
    apt-get install -y gettext && \
    apt install -y ncat && \
    python -m pip install --upgrade pip && \
    pip install poetry

COPY . $APP_HOME

RUN poetry config virtualenvs.create false
RUN poetry install --without dev

EXPOSE $DJANGO_FILM_ADMIN_PANEL_PORT

RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
