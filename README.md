# Cafe

A small website and back office for a coffee shop. Visitors get a landing page, a
menu and an account; staff get an admin panel where every piece of that content
is editable — dishes, categories, prices, photos, the landing copy, the employee
roster and the wording of every email.

Built with FastAPI, SQLAlchemy 2 (async), SQLAdmin, fastapi-users, fastapi-mail,
Taskiq and Jinja templates.

## Features

**Public site** — a landing page assembled from a single editable record (hero,
about text, contacts, amenities) and a menu grouped by category, with a detail
page for every dish. Sold-out items disappear from the menu automatically.

**Account pages** — register, log in, verify an address, request and set a new
password, sign out. Every fastapi-users endpoint except login expects JSON, so
the forms submit through `fetch` and render the error codes the API returns.
Pages live at the root (`/login`, `/account`); the API keeps its `/auth` and
`/users` prefixes.

**Admin panel** at `/admin` — CRUD for dishes, categories, employees, positions,
staff accounts, landing content and email texts. Russian labels, filters and
column formatting throughout.

**Role-based access** — two roles. Administrators manage everything; managers
work with the menu and read the staff directory but cannot touch staff accounts.
Sections a role cannot open disappear from the sidebar entirely.

**API accounts** — visitors register and log in over the API and get a JWT
bearer token. These accounts are separate from the staff accounts above: the
admin panel keeps its own session cookie, and the two contours share nothing but
password hashing. Customer records are visible in the admin panel but read-only,
apart from the flag that blocks an account.

**Transactional email** — address verification, a welcome note and a password
reset link. Sending happens in a Taskiq worker over RabbitMQ, so a slow SMTP
server never holds up a request. The wording of each message lives in the
database and is editable in the admin panel, while the HTML layout stays in the
repository, so copy changes need no deploy.

**Image uploads** go to S3-compatible storage. The database keeps the object key,
the template renders a full URL.

**Caching** in Redis, on two levels. Rendered HTML is stored per URL and dropped
whenever the underlying record changes in the admin panel, so edits show up
immediately instead of waiting for the TTL. Separately, the four fields the
header and footer need — name, address, phone, hours — are cached as JSON and
handed to every template through a context processor, so the shared chrome reads
from the database without querying it on each page.

## Running with Docker

```bash
cp .env.template .env
```

Fill in the blanks — the secrets and the S3 credentials — then:

```bash
docker compose up --build
```

This starts the app, a Taskiq worker, PostgreSQL, Redis, RabbitMQ and Mailpit.
Migrations run automatically on startup, so the only manual step is the first
administrator:

```bash
docker compose exec backend python -m scripts.create_staff -u admin -r ADMIN
```

Mailpit catches every outgoing message; read them at `http://localhost:8025`.

Templates and static files are mounted from the host, so edits to them show up
after a page refresh without rebuilding the image. Python code is not mounted —
changes there need `docker compose build backend`.

## Running locally

Requires Python 3.14, a running Redis and, if you want emails to leave the
queue, RabbitMQ. SQLite is used instead of PostgreSQL, so no database server is
needed.

```bash
cp .env.template .env
uv sync
uv run alembic upgrade head
uv run python -m scripts.create_staff -u admin -r ADMIN
uv run fastapi dev src/main.py
```

The password is asked interactively, so it never lands in your shell history.

The worker is a separate process:

```bash
uv run taskiq worker src.core.broker:broker --fs-discover --tasks-pattern "src/**/tasks.py"
```

## Pages

- `/` — landing page
- `/menu`, `/menu/{id}` — menu and dish details
- `/login`, `/register`, `/logout` — account access
- `/verify`, `/forgot-password`, `/reset-password` — reached from email links
- `/account` — the signed-in user's own record
- `/admin` — admin panel
- `/docs` — API docs (debug mode only)

The landing page needs its single record to exist before it renders; create it
from the admin panel on first run. The same record feeds the header and footer
on every page.

## Project layout

The codebase is split by responsibility rather than by file type.

```
src/
  core/      Infrastructure: settings, database, cache, storage, templates, hashing
  admin/     Admin panel building blocks: auth backend, base view, role mixin, filters
  cafe/      Menu domain: models, repository, routes, admin views
  staff/     Staff accounts and roles
  users/     API accounts: model, manager, auth backend, routers, admin view
  landing/   Landing page content and the shared cafe details
  mail/      Transactional email: message texts, SMTP client, sending service, tasks
templates/
  components/  Header and footer shared by every page
  users/       Account pages and their own stripped-down header
  landing/, cafe/, mail/, sqladmin/
static/      Stylesheet shared by the whole site
scripts/     One-off maintenance commands
```

`core` knows nothing about the domain, and `admin` knows nothing about coffee —
both can be lifted into another project unchanged. Domain modules own their own
models, repositories, routes and admin views, so a feature lives in one folder.

Page routes and API routes live in separate modules under `src/users/routers/`:
pages return HTML from the root, the API returns JSON under a prefix. Keeping
them apart is what lets both use plain names like `/login` and `/auth/login`.

## Development notes

Run scripts as modules from the project root, otherwise imports will not resolve:

```bash
uv run python -m scripts.create_staff --help
```

Admin panel templates in `templates/sqladmin/` override the ones shipped with
SQLAdmin. They extend the originals through the `sqladmin_original/` prefix, so
only the changed blocks are kept locally.

The landing page and the menu are cached, so template edits to them are not
visible until the cached response expires. While working on that markup, drop
the cache:

```bash
docker exec redis-cafe redis-cli FLUSHDB
```
