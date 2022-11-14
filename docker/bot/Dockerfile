FROM python:3.10.7-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/MagicHelper

RUN adduser --disabled-password --force-badname --gecos "" MagicHelper 
RUN usermod -a -G MagicHelper MagicHelper

ENV PROJECT_HOME=/home/MagicHelper/vk_bot
RUN mkdir -p ${PROJECT_HOME}
WORKDIR ${PROJECT_HOME}

COPY ./docker/ ./docker/
COPY ./app/ ./app/
COPY ./poetry.lock .
COPY ./pyproject.toml .
COPY ./Makefile .

RUN chmod +x ${PROJECT_HOME}/docker/bot/entrypoint.sh

RUN apt update
RUN apt install make
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir poetry
RUN python -m poetry config virtualenvs.create false
RUN python -m poetry install --no-dev

RUN chown -R MagicHelper:MagicHelper ${PROJECT_HOME}

USER MagicHelper

ENTRYPOINT ["/bin/sh", "/home/MagicHelper/vk_bot/docker/bot/entrypoint.sh"]