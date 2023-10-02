FROM python:3.10 as base

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update
RUN pip3 install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

FROM base as dev

RUN mkdir "opt/loyalty_fastapi_app"

COPY . /opt/loyalty_fastapi_app

WORKDIR /opt/loyalty_fastapi_app

EXPOSE 8006

CMD ["gunicorn", "src.main:app", "-w", "4" ,"-k", "uvicorn.workers.UvicornWorker", "-b 0.0.0.0:8006"]

