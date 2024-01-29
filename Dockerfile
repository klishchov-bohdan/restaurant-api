FROM python:3.10-slim

RUN mkdir /restaurant

WORKDIR restaurant

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

COPY . .

RUN mv .env.prod .env
RUN chmod a+x docker/*.sh
