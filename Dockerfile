FROM python:3.9.4-slim

LABEL MAINTAINER="Marcelo Lino <mdslino@gmail.com>"

ARG environment=production

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.6 \
    ENVIRONMENT=${environment}

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

RUN apt-get update && \
    if [ "$environment" = "production" ]; \
        then apt-get install --no-install-recommends --yes curl; \
    else apt-get install --no-install-recommends --yes curl make; fi && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && \
    if [ "$environment" = "production" ]; \
        then poetry install --no-dev --no-interaction --no-ansi; \
    else poetry install --no-interaction; fi

COPY . /app

EXPOSE 80