# Deployment Guide

## Local deployment
Use Django's development server for local testing:

```bash
python manage.py runserver
```

## Production notes

For a live deployment, use a production web server such as Gunicorn behind Nginx or a managed platform.

## Render

For the CareerPath Render web service, set these environment variables in the Render dashboard:

- `DEBUG=False`
- `DJANGO_SECRET_KEY` to a new, unique secret value (do not commit it)
- `ALLOWED_HOSTS=career-guidance-for-10th-students.onrender.com` (add any custom domains as comma-separated hostnames)
- `CSRF_TRUSTED_ORIGINS=https://career-guidance-for-10th-students.onrender.com` (add any custom HTTPS origins as comma-separated origins)
- `SECURE_SSL_REDIRECT=True`

The settings retain local development hosts and include the Render hostname by default; environment values add any extra hosts or trusted origins. The proxy SSL header and secure session/CSRF cookies are enabled for production when `DEBUG=False`.

Use this Render build command:

```text
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

Use this start command:

```text
gunicorn careerpath.wsgi:application
```

Keep the existing production database configuration and credentials. Render's free service filesystem is ephemeral, so SQLite is not suitable for durable user data. Check the existing database and migration state before applying migrations; do not run migrations against a replacement or unverified database.

## Recommended steps
1. Set `DEBUG=False` and provide a strong, unique `DJANGO_SECRET_KEY` through the deployment environment.
2. Configure `ALLOWED_HOSTS` with the deployment hostnames; do not use `*`.
3. Configure MySQL with `DB_ENGINE=mysql` and the `MYSQL_*` variables. The app will fail clearly instead of using SQLite if MySQL is unavailable.
4. Enable HTTPS at the deployment edge and verify secure cookie settings and proxy configuration for the chosen platform.
5. Review existing database and migration state, then run `python manage.py check --deploy`, `python manage.py showmigrations`, and reviewed migrations.
6. Run `python manage.py collectstatic` and use a production-grade WSGI/ASGI server behind the platform's supported proxy.
7. Run tests and verify the actual backend/database connection without disclosing credentials.

The settings enable HTTPS redirection and secure session and CSRF cookies when `DEBUG=False`. If TLS terminates at a reverse proxy, configure Django's secure-proxy setting only for a trusted proxy and test redirects to avoid loops. Review HSTS, backups, logging, and static/media storage for the specific hosting platform before launch.

## GitHub preparation
- Keep `.env` out of version control via `.gitignore`
- Commit only project code and documentation
- Use a secure deployment workflow for live credentials
