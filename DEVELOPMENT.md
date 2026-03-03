# Deployment & Production Setup

This document outlines the major steps required to transform the current development project into a production-ready application.

## 1. Configuration

- **Environment variables**: move all secrets, keys and toggles out of the source code. See `.env.example` for required vars.
- **Settings splitting**: you can create `beauty/settings_prod.py` that imports from `settings.py` and overrides DEBUG, DATABASES, etc.
- **Allowed hosts**: set `DJANGO_ALLOWED_HOSTS` appropriately (comma-separated list).

## 2. Database

- The `DATABASE_URL` environment variable controls the database connection (the project uses `dj-database-url`).
- For production, use PostgreSQL, MySQL or another managed service. Do **not** use SQLite in production.

## 3. Static & media files

- `collectstatic` gathers static assets into `STATIC_ROOT`. Configure the web server (Nginx) or a storage service (AWS S3) to serve them.
- Media files (uploaded images) should be stored in a persistent location like S3/Azure Blob/GCP Storage. You can use `django-storages`.

## 4. Containers

- A `Dockerfile` is provided to build the Python app image.
- `docker-compose.yml` sets up services for local development: a web container and a Postgres database.
- Example commands:
  ```bash
  cp .env.example .env
  docker-compose up --build
  docker-compose exec web python manage.py migrate
  docker-compose exec web python manage.py createsuperuser
  ```
- For production, push the built image to a registry (Docker Hub, GitHub Container Registry) and deploy using your chosen platform (ECS, Kubernetes, Heroku, etc.).

## 5. Server process & ASGI

- The image runs `gunicorn` with the `uvicorn` worker so Channels (WebSockets) are supported.
- Ensure your deployment supports ASGI and websockets (Heroku requires WebSocket-compatible stacks).

## 6. Domain & TLS

- Use a reverse proxy (Nginx/Caddy) or managed platform to terminate HTTPS.
- Renew certificates automatically (Let's Encrypt via Certbot or the hosting provider).

## 7. Monitoring & Logging

- Add Sentry or similar for error tracking.
- Configure log aggregation (stdout to Docker logs or external service).

## 8. Scaling & background jobs

- If you add asynchronous tasks (e.g., email notifications), integrate Celery + Redis/RabbitMQ.

## 9. Frontend

- Build React assets for production (`npm run build`) and serve them as static files or host separately.
- Consider deploying the frontend to Vercel/Netlify and using the API URL as an environment variable.

## 10. Security

- Set `SECURE_BROWSER_XSS_FILTER`, `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS`, etc. via middleware.
- Use `django-cors-headers` if your API is consumed from other origins.
- Turn off debug, use strong passwords, and keep dependencies updated.

---

This file is a starting point; adapt each section to your chosen infrastructure and requirements.