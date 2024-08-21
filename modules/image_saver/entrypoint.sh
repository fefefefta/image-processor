#!/bin/sh

if [ "$(alembic current)" = "None" ]; then
  echo "Создание первой миграции..."
  alembic revision --autogenerate -m "Initial migration"
fi

alembic upgrade head

python src/main.py
