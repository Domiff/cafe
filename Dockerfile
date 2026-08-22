FROM python:3.14-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /uvx /bin/
ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_NO_DEV=1

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --locked

WORKDIR /app

COPY . .

RUN chmod +x run.sh
RUN chmod +x taskiq.sh

EXPOSE 8080
