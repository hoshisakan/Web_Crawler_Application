# FROM python:3.7.9
FROM python:3.7.9
#TODO For log message in container
ENV PYTHONUNBUFFERED 1

RUN cd / && ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    vim \
    tree

RUN apt-get install -y \
    gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 \
    libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation \
    libappindicator1 libnss3 lsb-release xdg-utils

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
RUN rm -f google-chrome-stable_current_amd64.deb

WORKDIR /backend
COPY requirements.txt /backend/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR /backend/crawler