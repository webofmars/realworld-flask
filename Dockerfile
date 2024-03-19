FROM python:3.10-slim-buster

ARG TARGETARCH

# https://github.com/krallin/tini
ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini-${TARGETARCH} /tini

RUN chmod a+x /tini \
    && pip3 install --no-cache pipenv poetry

# Set the environment variable for poetry
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

COPY /realworld /app/realworld
COPY /alembic /app/alembic
COPY alembic.ini /app/
COPY /scripts/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# Set the entry point to the script
ENTRYPOINT ["/entrypoint.sh"]