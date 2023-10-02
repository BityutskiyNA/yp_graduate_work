FROM python:3.10 as base

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update
RUN pip3 install --upgrade pip

COPY ./requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

FROM base as dev

RUN mkdir "opt/ugc_etl"

COPY ./src /opt/ugc_etl

WORKDIR /opt/ugc_etl

CMD ["python", "/opt/ugc_etl/main.py"]

