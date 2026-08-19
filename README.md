# Cafe

A small website and back office for a coffee shop. Visitors get a landing page and
a menu; staff get an admin panel where every piece of that content is editable —
dishes, categories, prices, photos, the landing copy, and the employee roster.

Built with FastAPI, SQLAlchemy 2 (async), SQLAdmin and Jinja templates.

## Features

**Public site** — a landing page assembled from a single editable record (hero,
about text, contacts, amenities) and a menu grouped by category, with a detail
page for every dish. Sold-out items disappear from the menu automatically.

**Admin panel** at `/admin` — CRUD for dishes, categories, employees, positions,
staff accounts and landing content. Russian labels, filters and column formatting
throughout.

**Role-based access** — two roles. Administrators manage everything; managers
work with the menu and read the staff directory but cannot touch staff accounts.
Sections a role cannot open disappear from the sidebar entirely.

**Image uploads** go to S3-compatible storage. The database keeps the object key,
the template renders a full URL.

**Page caching** in Redis. Rendered HTML is stored per URL and dropped
automatically whenever the underlying record changes in the admin panel, so edits
show up immediately instead of waiting for the TTL.

## Configuration

Both ways of running the project read the same `.env` file in the project root:

```
APP_PORT=8080

SECRET_KEY=<random string, e.g. `python -c "import secrets; print(secrets.token_urlsafe(32))"`>

POSTGRES_DB=cafe
POSTGRES_USER=cafe
POSTGRES_PASSWORD=<password>
POSTGRES_HOST=pg
POSTGRES_PORT=5432

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
EXPIRE=3600

AWS_ACCESS_KEY_ID=<key>
AWS_SECRET_ACCESS_KEY=<secret>
AWS_S3_BUCKET_NAME=<bucket>
AWS_S3_ENDPOINT_URL=<host, without the protocol>
AWS_DEFAULT_ACL=public-read
AWS_S3_USE_SSL=True

LOGTAIL_TOKEN=<token>
LOGTAIL_HOST=<host>
```

`SECRET_KEY` signs admin session cookies, and the Logtail pair is required at
startup — set them even when you are only trying the project out. Everything else
has a working default.

`IS_DOCKERIZED` decides where the app looks for its dependencies: when it is set,
PostgreSQL replaces SQLite and the Redis host becomes the compose service name.
Docker Compose sets it for you; leave it alone when running locally.

## Running with Docker

```bash
docker compose up --build
```

This starts the app, PostgreSQL and Redis. Migrations run automatically on
startup, so the only manual step is the first administrator:

```bash
docker compose exec backend python -m scripts.create_staff -u admin -r ADMIN
```

Templates and static files are mounted from the host, so edits to them show up
after a page refresh without rebuilding the image.

## Running locally

Requires Python 3.14 and a running Redis. SQLite is used instead of PostgreSQL,
so no database server is needed.

```bash
uv sync
uv run alembic upgrade head
uv run python -m scripts.create_staff -u admin -r ADMIN
uv run fastapi dev src/main.py
```

The password is asked interactively, so it never lands in your shell history.

## Pages

- `/` — landing page
- `/menu` — menu
- `/admin` — admin panel
- `/docs` — API docs (debug mode only)

The landing page needs its single record to exist before it renders; create it
from the admin panel on first run.

## Project layout

The codebase is split by responsibility rather than by file type.

```
src/
  core/      Infrastructure: settings, database, cache, storage, templates, hashing
  admin/     Admin panel building blocks: auth backend, base view, role mixin, filters
  cafe/      Menu domain: models, repository, routes, admin views
  staff/     Staff accounts and roles
  landing/   Landing page content
templates/   Jinja templates, including sqladmin overrides
static/      Stylesheet shared by the landing page and the menu
scripts/     One-off maintenance commands
```

`core` knows nothing about the domain, and `admin` knows nothing about coffee —
both can be lifted into another project unchanged. Domain modules own their own
models, repositories, routes and admin views, so a feature lives in one folder.

## Development notes

Run scripts as modules from the project root, otherwise imports will not resolve:

```bash
uv run python -m scripts.create_staff --help
```

Admin panel templates in `templates/sqladmin/` override the ones shipped with
SQLAdmin. They extend the originals through the `sqladmin_original/` prefix, so
only the changed blocks are kept locally.
