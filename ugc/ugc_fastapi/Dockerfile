FROM python:3.9 as base

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update
RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

FROM base as dev

RUN mkdir "opt/ugc_fastapi_app"

COPY src /opt/ugc_fastapi_app
COPY tests /opt/ugc_fastapi_app/tests

WORKDIR /opt/ugc_fastapi_app

EXPOSE 8002

CMD ["gunicorn", "main:app", "-w", "4" ,"-k", "uvicorn.workers.UvicornWorker", "-b 0.0.0.0:8002"]

