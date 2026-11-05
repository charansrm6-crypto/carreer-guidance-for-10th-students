# Installation Guide

## Python setup
1. Install Python 3.12 or newer.
2. Create a virtual environment: `python -m venv .venv`
3. Activate the environment:
   - Windows: `.venv\Scripts\activate`

## Install dependencies
Run:

```bash
python -m pip install -r requirements.txt
```

## Environment variables
Create `.env` from `.env.example` and set the values as needed. The project defaults to SQLite for local testing. `DEBUG` defaults to `False` in application settings; set it to `True` only for local development.

```env
DB_ENGINE=sqlite
DJANGO_SECRET_KEY=replace-with-a-generated-random-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Generate a local secret with Django's `get_random_secret_key()` utility or another trusted secret generator. Keep the value private and do not commit `.env`. For development only, a random temporary key is generated if no key is configured; production (`DEBUG=False`) requires `DJANGO_SECRET_KEY`.

For MySQL, set `DB_ENGINE=mysql` and configure:

```env
DB_ENGINE=mysql
MYSQL_DATABASE=career
MYSQL_USER=replace-with-mysql-user
MYSQL_PASSWORD=replace-with-mysql-password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

When MySQL is explicitly selected, Django does not fall back to SQLite. A failed connection is an environment or database configuration error and should be diagnosed rather than bypassed.

## Migrations
Run:

```bash
python manage.py check
python manage.py showmigrations
python manage.py migrate
```

Before migrating an existing database, verify the selected backend and database name, and retain a suitable backup. Do not use destructive database reset commands.

## Seed data
Load initial sample data:

```bash
python manage.py seed_data
```

The command creates missing starter records and is safe to rerun; it does not overwrite content already present in the database. Review and maintain content through Django Admin. Starter scholarship, examination, and admission information is general guidance and must be checked against current official notices.

## Run the app
```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## ECE guidance
The ECE guidance page describes general study paths and career areas. Admission requirements, lateral-entry rules, recognition, and professional eligibility vary and must be checked with current official institutional notifications.
