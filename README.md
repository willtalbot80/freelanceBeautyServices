# freelanceBeautyServices
App where freelance beauty experts can get bookings

## Quickstart (development)

### Running with Docker (recommended)

A `Dockerfile` and `docker-compose.yml` are included to simplify local development and production deployment.

1. Build and start services:

```bash
# from repository root
cp .env.example .env           # create your own environment file
npm install --prefix frontend   # optional frontend build

docker-compose up --build
```

2. The Django app will be available at http://localhost:8000/ and PostgreSQL runs in a container.

3. To run migrations inside the web container:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

(Static files are collected during the image build.)

### Environment variables

#### Firebase (frontend)

If you want to use Firebase authentication or services, add the following values to the frontend environment (create `.env.local` inside `frontend/`):

```env
REACT_APP_FIREBASE_API_KEY=your_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=your-app.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-app.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=xxxxxxx
REACT_APP_FIREBASE_APP_ID=1:xxxx:web:abcdefg
```

Then the React code (see `frontend/src/firebase.js`) will initialize the SDK and you can use `firebaseAuth` to sign users in.
#### Firebase Admin (backend)

To allow Django to verify tokens you will need a service account key. Set the
`FIREBASE_ADMIN_CREDENTIAL` environment variable to either the raw JSON
credential string or the path to a downloaded JSON file. Example in `.env`:

```env
FIREBASE_ADMIN_CREDENTIAL='{"type": "service_account", ... }'
```

After that, requests bearing `Authorization: Bearer <ID_TOKEN>` will be
authenticated via Firebase and a corresponding Django user will be created.

Docker / secrets
----------------

When running with Docker Compose you can mount your service account JSON
into the container and point `FIREBASE_ADMIN_CREDENTIAL` at that path.

Example `docker-compose.yml` snippet (the repository includes a variant):

```yaml
services:
	web:
		volumes:
			- ./secrets/firebase-sa.json:/run/secrets/firebase-sa.json:ro
		environment:
			- FIREBASE_ADMIN_CREDENTIAL=/run/secrets/firebase-sa.json
```

You can validate the mounted credential using the Django management
command `validate_firebase_sa`:

```bash
# validate using the mounted file
python manage.py validate_firebase_sa --file ./secrets/firebase-sa.json --list-users
```

This command will initialize the Firebase Admin SDK with the supplied
credential and (optionally) attempt a lightweight API call to confirm
access.

### Environment variables

Create a `.env` file with at least:

```env
DJANGO_SECRET_KEY=replace-with-secure-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://django:password123@db:5432/beauty
```

More details on production configuration are in the `DEVELOPMENT.md` file.

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set the Django secret key (export or set in environment):

```bash
export DJANGO_SECRET_KEY='replace-with-a-secure-key'
```

3. Run migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Run the development server:

```bash
python manage.py runserver
```

The admin is available at http://127.0.0.1:8000/admin/ and the default DB is SQLite.

Next steps: implement API endpoints, upload handling, and real-time chat with Channels.

### Deployment hints

A `Dockerfile` and `docker-compose.yml` accompany the project to help you containerise the application. Use environment variables (see `.env.example`) to manage secrets and database settings. The production server should run with `DEBUG=False` and behind a reverse proxy (e.g., Nginx) serving HTTPS.

Media uploads:

- This project uses `ImageField` for avatars and portfolio images. Install `Pillow` (included in `requirements.txt`).
- In development, media files are served when `DEBUG=True` by the URLs added to `beauty/urls.py`.
- Uploaded portfolio images are available under `/media/portfolio/`.

To upload a portfolio image via the API (authenticated expert user):

```bash
# obtain a token
curl -X POST -d "username=expert&password=secret" http://127.0.0.1:8000/api-token-auth/

# upload a file (replace TOKEN and path)
curl -H "Authorization: Token TOKEN" -F "image=@/path/to/photo.jpg" -F "caption=Before/After" \
	http://127.0.0.1:8000/api/portfolio-images/
```

Registration endpoint:

```bash
# create an account and receive a token
curl -X POST -H "Content-Type: application/json" -d '{"username":"alice","password":"secret","is_expert":true}' \
	http://127.0.0.1:8000/api/register/
```

Browse experts in the browser at http://127.0.0.1:8000/ and click an expert to view their portfolio.

