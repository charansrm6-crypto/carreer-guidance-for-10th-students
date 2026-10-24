# Deployment Guide

## Local deployment
Use Django's development server for local testing:

```bash
python manage.py runserver
```

## Production notes
For a live deployment, use a production web server such as Gunicorn behind Nginx or a managed platform.

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
