FROM python:3.7.4-alpine3.10
ENV PYTHONUNBUFFERED 1
RUN apk add gcc musl-dev python3-dev
RUN pip install cython
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/