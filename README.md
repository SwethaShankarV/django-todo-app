# Django ToDo App

A simple task manager built with Django that lets users:

- Sign up and log in with Django's auth system
- Add, edit, and delete personal todo items
- See tasks in a clean, responsive UI styled with custom CSS
- Keep tasks scoped per user using a `TODOO` model linked to `django.contrib.auth.User`

## Tech Stack

- Django 6
- Python 3.12
- HTML + CSS (Poppins font, Font Awesome)
- SQLite (dev)

Run locally:

```bash
pip install -r requirements.txt  # if you add one
python manage.py migrate
python manage.py runserver
