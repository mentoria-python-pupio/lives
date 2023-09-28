FROM python:3.11-slim-buster

RUN apt-get update -y

RUN apt-get install python3-dev build-essential vim -y

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install

COPY . /app/

CMD ["poetry", "run", "python", "timer_bot_telegram.py"]