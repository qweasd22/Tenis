@echo off
set DEBUG=True
set ALLOWED_HOSTS=localhost,127.0.0.1,testserver
set SECURE_SSL_REDIRECT=False
set SESSION_COOKIE_SECURE=False
set CSRF_COOKIE_SECURE=False
set PYTHONIOENCODING=utf-8

if exist ..\venv\Scripts\python.exe (
    ..\venv\Scripts\python.exe manage.py runserver
) else (
    python manage.py runserver
)
