# CareerPath

CareerPath is a Django web application designed to guide students after the 10th class by providing information on streams, careers, courses, scholarships, and entrance examinations.

## Features

- Student registration and authentication
- Protected student dashboard
- After-10th roadmap and detail pages
- Career, course, scholarship, and exam listings
- Team information and contact form
- Dedicated ECE pathway and career guidance
- Search and filtering across major sections
- Responsive and beginner-friendly design
- Django admin support

## Technology stack

- Python 3.12
- Django 5.x
- MySQL support via environment variables
- SQLite fallback for local development and testing
- HTML, CSS, and JavaScript

## Quick start

1. Create a virtual environment
   - `python -m venv .venv`
2. Activate it
   - Windows: `.venv\Scripts\activate`
3. Install dependencies
   - `python -m pip install -r requirements.txt`
4. Configure environment variables
   - Copy `.env.example` to `.env` and update values as needed.
5. Apply migrations
   - `python manage.py migrate`
6. Load sample data
   - `python manage.py seed_data`
7. Run the development server
   - `python manage.py runserver`

## Admin

- Create a superuser with `python manage.py createsuperuser`
- Open `/admin/` to manage the project content

## Testing

- Run project checks: `python manage.py check`
- Run tests: `python manage.py test`

## Notes

- The project uses `DB_ENGINE=sqlite` by default in `.env` for local usage.
- To use MySQL, set `DB_ENGINE=mysql` and provide the MySQL credentials in `.env`.
- MySQL selection does not silently fall back to SQLite; verify the live connection before considering the database configured.
- Scholarship, exam, admission, and eligibility details should be confirmed through current official sources.
