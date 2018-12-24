FROM ubuntu:16.04

RUN mkdir app

RUN apt-get update -qq && apt-get install -y \
    mongodb-shell \
    mongodb-tools \
    python3.6 \
    python3-pip \
    python3.6-dev \
    nano

RUN python3.6 -m pip install --upgrade pip

RUN mkdir /app/telegram

COPY nginx.conf /etc/nginx/sites-enabled/telegram.conf
COPY supervisord.conf /etc/supervisor/conf.d/telegram.conf

ADD api /app/telegram
ADD setup.py /app

WORKDIR /app

RUN mkdir /var/log/microservices/telegram

RUN chmod 755 /app/setup.py
RUN /app/setup.py develop
