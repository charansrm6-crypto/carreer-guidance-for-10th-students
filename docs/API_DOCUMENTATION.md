# API Documentation

This project is primarily a Django template application and does not expose a separate REST API by default.

## Routes
- `/` – Home page
- `/register/` – Student registration
- `/login/` – Student login
- `/dashboard/` – Authenticated student dashboard
- `/roadmaps/` – Roadmap listing
- `/roadmap/<slug>/` – Roadmap detail
- `/careers/` – Career listing
- `/career/<slug>/` – Career detail
- `/courses/` – Course listing
- `/course/<slug>/` – Course detail
- `/scholarships/` – Scholarship listing
- `/scholarship/<slug>/` – Scholarship detail
- `/exams/` – Entrance exam listing
- `/exam/<slug>/` – Entrance exam detail
- `/ece-guidance/` – ECE pathways and career guidance
- `/team/` – Team page
- `/about/` – About page
- `/contact/` – Contact form page
- `/admin/` – Admin interface
- `/admin-messages/` – Staff-only contact-message listing

## Notes
The site uses standard HTML forms and server-side validation without a separate JavaScript API layer.
Search terms and selected list filters are validated server-side. Invalid detail slugs return 404 responses. Logout requires a CSRF-protected POST request.
