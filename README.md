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
users and landing content. Russian labels, filters and column formatting
throughout.

**Role-based access** — two roles. Administrators manage everything; managers
work with the menu and read the staff directory but cannot touch user accounts.
Sections a role cannot open disappear from the sidebar entirely.

**Image uploads** go to S3-compatible storage. The database keeps the object key,
the template renders a full URL.

**Page caching** in Redis. Rendered HTML is stored per URL and dropped
automatically whenever the underlying record changes in the admin panel, so edits
show up immediately instead of waiting for the TTL.

## Requirements

- Python 3.14
- Redis (page cache)
- An S3-compatible bucket (image uploads)

SQLite is used by default, so no database server is needed to get started.

## Getting started

Install dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```
CAFE_SECRET_KEY=<random string, e.g. `python -c "import secrets; print(secrets.token_urlsafe(32))"`>

CAFE_LOGTAIL_TOKEN=<logtail token>
CAFE_LOGTAIL_HOST=<logtail host>

CAFE_AWS_ACCESS_KEY_ID=<key>
CAFE_AWS_SECRET_ACCESS_KEY=<secret>
CAFE_AWS_S3_BUCKET_NAME=<bucket>
CAFE_AWS_S3_ENDPOINT_URL=<host, without the protocol>
CAFE_AWS_DEFAULT_ACL=public-read
CAFE_AWS_S3_USE_SSL=True
```

Every setting is read with a `CAFE_` prefix. Database, Redis and debug options
have sensible defaults and only need to be set when you deviate from them.

Apply migrations:

```bash
uv run alembic upgrade head
```

Create the first administrator:

```bash
uv run python -m scripts.create_user -u admin -r ADMIN
```

The password is asked interactively, so it never lands in your shell history.

Run the app:

```bash
uv run fastapi dev src/main.py
```

- `/` — landing page
- `/menu` — menu
- `/admin` — admin panel
- `/docs` — API docs (debug mode only)

The landing page needs its single record to exist before it renders; create it
from the admin panel on first run.

## Configuration

| Prefix group | Purpose |
|---|---|
| `CAFE_IS_DEBUG`, `CAFE_IS_DOCKERIZED` | Environment switches. `IS_DOCKERIZED` swaps SQLite for PostgreSQL and `localhost` for in-cluster hostnames. |
| `CAFE_SQLITE_URL`, `CAFE_POSTGRES_*` | Database connection. |
| `CAFE_REDIS_*`, `CAFE_EXPIRE` | Cache backend and default TTL. |
| `CAFE_AWS_*` | S3 credentials, bucket and ACL. |
| `CAFE_SECRET_KEY` | Signs admin session cookies. |
| `CAFE_LOGTAIL_*` | Log shipping. |

## Project layout

The codebase is split by responsibility rather than by file type.

```
src/
  core/      Infrastructure: settings, database, cache, storage, templates
  admin/     Admin panel building blocks: auth backend, base view, role mixin, filters
  cafe/      Menu domain: models, repository, routes, admin views
  auth/      Users, roles, password hashing
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
uv run python -m scripts.create_user --help
```

Admin panel templates in `templates/sqladmin/` override the ones shipped with
SQLAdmin. They extend the originals through the `sqladmin_original/` prefix, so
only the changed blocks are kept locally.
