# Veículos Rest API

## Features

- FastAPI
- ORM (sqlmodel)

## Requirements

- Poetry (https://python-poetry.org/)
  - Or some virtual environment manager of your choice

## Setup and install

- Copy `.env.example` -> `.env` and edit according to your needs
- Run `poetry install`

## Start development server

### Docker

- Run `docker compose up --build`
  - Go to `http://localhost:[.env PORT]/docs` to access the API Docs

### Local

- Run `poetry run granian --interface asgi app.server:app`

## Documentation

Go to `/docs` to access swagger auto-generated docs.

## Tests

- Run `poetry run pytest`
