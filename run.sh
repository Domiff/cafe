#!/bin/sh
uv run alembic upgrade head
uv run fastapi run --port "${APP_PORT}"
