# Lightweight Python image
FROM python:3.12-slim

# set working directory
WORKDIR /app

# install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
  && rm -rf /var/lib/apt/lists/*

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn","beauty.asgi:application","-k","uvicorn.workers.UvicornWorker","--bind","0.0.0.0:8000"]
