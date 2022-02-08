FROM python:3.9.7-slim-buster as base_build

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/usr/src/poetry" \
    PYTHONPATH="/application " \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/usr/src/pysetup" \
    VENV_PATH="/usr/src/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

RUN apt-get install -y locales locales-all

ENV POETRY_VERSION=1.1.12
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev  # respects

WORKDIR /application
COPY . /application
EXPOSE 8000