FROM python:3.14-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_PROJECT_ENVIRONMENT=/usr/local
ENV UV_NO_DEV=1

COPY ./pyproject.toml ./uv.lock ./
RUN uv sync --locked

WORKDIR /app

COPY . .

RUN chmod +x run.sh

EXPOSE 8080

CMD ["./run.sh"]
