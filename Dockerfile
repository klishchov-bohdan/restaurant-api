FROM python:3.10

RUN mkdir /restaurant

WORKDIR restaurant

COPY . .

RUN pip install -r requirements.txt

RUN mv .env.prod .env
#RUN chmod a+x docker/*.sh
