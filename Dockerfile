FROM python:3.10-slim-buster

RUN apt-get update \
    && apt-get install -y curl

RUN pip install -U pip \
    && pip install --no-cache pipenv \
    && pip install --no-cache poetry

COPY poetry.lock pyproject.toml /app/

WORKDIR /app

RUN poetry config virtualenvs.create false \
    && poetry install --with dev

ENTRYPOINT ["/bin/bash"]