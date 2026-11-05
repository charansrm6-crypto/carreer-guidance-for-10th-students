CareerPath - Render deployment fix
===================================

The deployed URL hostname is:
carreer-guidance-for-10th-students.onrender.com
("carreer" is spelled with double r after "ca").

Updated in this ZIP:
1. settings.py default ALLOWED_HOSTS hostname corrected.
2. settings.py default CSRF_TRUSTED_ORIGINS origin corrected.
3. Existing comma-separated environment parsing and validation retained.
4. WhiteNoise STORAGES configuration added.
5. Existing WhiteNoise middleware and whitenoise requirement retained.
6. Deployment documentation updated.

Set these Render Environment values:
ALLOWED_HOSTS=carreer-guidance-for-10th-students.onrender.com
CSRF_TRUSTED_ORIGINS=https://carreer-guidance-for-10th-students.onrender.com
DB_ENGINE=sqlite
DEBUG=False
DJANGO_SECRET_KEY=<keep your existing secret in Render>

Render Build Command:
pip install -r requirements.txt && python manage.py collectstatic --no-input

Render Start Command:
gunicorn careerpath.wsgi:application --bind 0.0.0.0:$PORT

Important:
- Also correct ALLOWED_HOSTS in the Render Dashboard; changing files alone
  does not change Render's environment variables.
- Do not put DJANGO_SECRET_KEY in GitHub or this ZIP.
- This ZIP intentionally excludes real .env files, .git history, and db.sqlite3.
- SQLite on Render's free filesystem is ephemeral; use persistent PostgreSQL
  if student accounts/data must survive restarts and redeploys.

Validation:
- settings.py passed Python syntax parsing.
- Full Django checks, migrations, and live Render deployment were not run here.
