# Cafe

A small website and back office for a coffee shop. Visitors get a landing page and
a menu; staff get an admin panel where every piece of that content is editable —
dishes, categories, prices, photos, the landing copy, and the employee roster.

Built with FastAPI, SQLAlchemy 2 (async), SQLAdmin, fastapi-users, fastapi-mail
and Jinja templates.

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

**API accounts** — visitors register and log in over the API and get a JWT
bearer token. These accounts are separate from the staff accounts above: the
admin panel keeps its own session cookie, and the two contours share nothing but
password hashing. Customer records are visible in the admin panel but read-only,
apart from the flag that blocks an account.

**Transactional email** — an SMTP client and a sending service for the messages
the site needs: address verification, a welcome note, a password reset link. The
wording of each one lives in the database and is editable in the admin panel,
while the HTML layout stays in the repository, so copy changes need no deploy. A
fresh database starts with an empty table; the texts are filled in from the admin
panel.

**Image uploads** go to S3-compatible storage. The database keeps the object key,
the template renders a full URL.

**Page caching** in Redis. Rendered HTML is stored per URL and dropped
automatically whenever the underlying record changes in the admin panel, so edits
show up immediately instead of waiting for the TTL.

## Configuration

Both ways of running the project read the same `.env` file in the project root:

```
APP_PORT=8080

ADMIN_SECRET_KEY=<random string, e.g. `python -c "import secrets; print(secrets.token_urlsafe(32))"`>

STRATEGY_SECRET_KEY=<random string>
RESET_SECRET_KEY=<another one>
VERIFICATION_SECRET_KEY=<and another>

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

BASE_URL=http://localhost:8000

MAIL_USERNAME=<smtp login>
MAIL_PASSWORD=<smtp password>
MAIL_FROM=no-reply@example.com
MAIL_SERVER=localhost
MAIL_PORT=1025
MAIL_STARTTLS=false
MAIL_SSL_TLS=false
USE_CREDENTIALS=true
VALIDATE_CERTS=true
```

`ADMIN_SECRET_KEY` signs admin session cookies and the three user secrets sign
API tokens; together with the Logtail pair they are required at startup, so set
them even when you are only trying the project out. Use a different value for
each. Everything else has a working default.

`BASE_URL` is the origin used to build links inside emails, so it has to match
the address people actually open. The mail settings have no defaults either.
During development point them at a local fake SMTP such as Mailpit
(`localhost:1025`, both TLS flags off, no credentials); in production use a real
server, where port 465 means `MAIL_SSL_TLS=true` and port 587 means
`MAIL_STARTTLS=true` — never both.

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
- `/auth/register`, `/auth/login`, `/auth/logout` — API accounts
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
  users/     API accounts: model, manager, auth backend, admin view
  landing/   Landing page content
  mail/      Transactional email: message texts, SMTP client, sending service
templates/   Jinja templates, including sqladmin overrides and the email layout
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
