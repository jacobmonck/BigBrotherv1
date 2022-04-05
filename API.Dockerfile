FROM python:3.10

WORKDIR /api

# RUN apt update && apt install -y gcc

RUN pip install poetry

COPY pyproject.toml /api
COPY poetry.lock /api

RUN poetry install

COPY . /api

CMD ["poetry", "run", "task", "api"]