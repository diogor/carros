FROM python:3.13

RUN pip install poetry

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY . /app/

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["granian", "--interface", "asgi", "app.server:app", "--port", "8080", "--host", "0.0.0.0"]
