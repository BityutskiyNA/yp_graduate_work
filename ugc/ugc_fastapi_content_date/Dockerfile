FROM python:3.9 as base

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update
RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

FROM base as dev

RUN mkdir "opt/src"

COPY src /opt/src
COPY tests /opt/src/tests

WORKDIR /opt/src

EXPOSE 8003

CMD ["gunicorn", "main:app", "-w", "4" ,"-k", "uvicorn.workers.UvicornWorker", "-b 0.0.0.0:8002"]

