# Project Documentation

## Overview
CareerPath is a student guidance website focused on helping 10th-class students understand educational pathways after school and plan their career journey wisely.

## Problem statement
Students usually face uncertainty after 10th class because they are not fully aware of streams, alternatives, scholarships, and career opportunities. The goal is to present this information clearly and accessibly.

## Objectives
- Provide guidance on career exploration
- Explain after-10th education options
- Offer course and scholarship awareness
- Support entrance exam awareness
- Create a clean, responsive, student-friendly platform

## Features
- Student login and registration
- Protected dashboard
- Roadmap, career, course, scholarship, and exam modules
- Contact form for user communication
- Team section and WhatsApp group support
- Django admin management
- Dedicated ECE pathways and career-area guidance

## Architecture
The project uses Django's model-view-template architecture, keeping business logic in views and data in models. Templates and static files provide the frontend presentation.

The ECE page is general guidance, not an admission or employment guarantee. Students should verify current entrance, eligibility, lateral-entry, and recognition rules with official institutions.

## Database design
Main entities include `Student`, `Roadmap`, `Career`, `Course`, `Scholarship`, `EntranceExam`, `TeamMember`, and `ContactMessage`.

## Installation
See `docs/INSTALLATION.md` for step-by-step local setup instructions.

## Testing
Use Django's `manage.py check` and `manage.py test` commands for verification.
