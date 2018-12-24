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

RUN mkdir /app/emailer

COPY nginx.conf /etc/nginx/sites-enabled/emailer.conf
COPY supervisord.conf /etc/supervisor/conf.d/emailer.conf

ADD api /app/emailer
ADD setup.py /app

WORKDIR /app

RUN mkdir /var/log/microservices/emailer

RUN chmod 755 /app/setup.py
RUN /app/setup.py develop
