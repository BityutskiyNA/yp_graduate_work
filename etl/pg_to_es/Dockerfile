# base image
FROM python:3.10-slim

# enviironment variables
ENV APP_HOME=/etl/pg_to_es
# enviironment variables
# create app directory
WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && \
    apt-get install -y gettext && \
    apt install -y ncat && \
    python -m pip install --upgrade pip && \
    pip3 install poetry

COPY . $APP_HOME

RUN poetry config virtualenvs.create false
RUN poetry install --without dev

RUN chmod +x ./docker-entrypoint.dev.sh

ENTRYPOINT ["./docker-entrypoint.dev.sh"]