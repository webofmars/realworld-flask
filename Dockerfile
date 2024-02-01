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

# Copy only the necessary files to avoid reinstalling dependencies on code changes
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy the entire project
COPY /realworld /app/realworld

ENTRYPOINT ["/tini", "--"]
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=8080"]
