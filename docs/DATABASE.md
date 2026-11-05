# Database Guide

## Default setup
The project uses SQLite when `DB_ENGINE=sqlite`. This is suitable for local development and tests. The selected backend is controlled by the environment; unsupported engine values produce a configuration error.

## MySQL setup
When `DB_ENGINE=mysql` is configured, Django connects to the configured `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, and `MYSQL_PORT` values. The intended database name is `career`. A missing or unavailable MySQL server is reported as a connection failure; the application does not silently switch to SQLite.

## Important notes
- Never hard-code production credentials.
- Keep `.env` local and uncommitted.
- Use the official Django migration system rather than manual SQL updates.

## Migration workflow
```bash
python manage.py check
python manage.py showmigrations
python manage.py migrate
```

Inspect the active database before applying migrations. `showmigrations` reports migration history, not whether the intended MySQL server is reachable. To verify the selected backend and database name and make a live connection without printing credentials, run:

```bash
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print(connection.vendor, connection.settings_dict['NAME'])"
```

Do not run `flush`, database drops, or reset commands against databases that may contain existing project or student data. Create migrations only when model changes require them and review them before applying.

## Inspection
This project can inspect the database using Django shell tools or MySQL client tools if available.
