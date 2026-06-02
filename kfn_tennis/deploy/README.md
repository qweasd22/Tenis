# Production Deploy Notes

1. Copy `.env.example` to `.env` and replace domain, `SECRET_KEY`, hosts, and security values.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run migrations: `python manage.py migrate`.
4. Collect static files: `python manage.py collectstatic --noinput`.
5. Put the project at `/var/www/kfn_tennis` or update paths in `deploy/*.service` and `deploy/nginx.conf`.
6. Enable the systemd service and nginx site.

Keep `SECURE_SSL_REDIRECT=True` and HSTS enabled only after HTTPS certificates are working.
