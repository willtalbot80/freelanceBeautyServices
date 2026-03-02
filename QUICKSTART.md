# Freelance Beauty Services — Quick Start Guide

A full-stack freelance beauty booking app with Firebase authentication, Django REST API, and React frontend.

## 📋 Prerequisites

- Python 3.12+
- Node.js 16+
- Firebase project (for authentication)
- Git

## 🚀 Quick Setup (Local Development)

### 1. Clone and Initialize

```bash
git clone https://github.com/willtalbot80/freelanceBeautyServices
cd freelanceBeautyServices

# Set up Python virtual environment
python -m venv .venv
source .venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Set up frontend
cd frontend
npm install
cd ..
```

### 2. Configure Environment Variables

**Backend (.env file in project root):**

```bash
cp .env.example .env
```

Edit `.env`:
```env
DJANGO_SECRET_KEY=your-secure-random-key-here-min-50-chars
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
# FIREBASE_ADMIN_CREDENTIAL is optional for development
```

**Frontend (frontend/.env.local):**

```bash
cp frontend/.env.local.example frontend/.env.local
```

Edit `frontend/.env.local` with your Firebase credentials from [Firebase Console](https://console.firebase.google.com):

```env
REACT_APP_FIREBASE_API_KEY=xxx
REACT_APP_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=xxx
REACT_APP_FIREBASE_APP_ID=1:xxx:web:xxx
```

### 3. Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser  # Create admin user
```

### 4. Seed Demo Data (Optional)

```bash
python manage.py shell
```

Then in the Python shell:

```python
from django.contrib.auth import get_user_model
from experts.models import ExpertProfile, PortfolioImage
from PIL import Image
import io

User = get_user_model()

# Create demo expert user
expert_user = User.objects.create_user(
    username='demo_expert',
    email='expert@example.com',
    password='password123',
    is_expert=True
)

# Create expert profile
profile = ExpertProfile.objects.create(
    user=expert_user,
    service_type='makeup',
    hourly_rate=50.00,
    availability_notes='Available Tuesdays-Saturdays'
)

# Create a placeholder portfolio image
img = Image.new('RGB', (400, 300), color='#D4A574')
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

from django.core.files.uploadedfile import InMemoryUploadedFile
portfolio_pic = PortfolioImage.objects.create(
    expert=profile,
    image=InMemoryUploadedFile(
        img_bytes, None, 'demo.jpg', 'image/jpeg', img_bytes.getbuffer().nbytes, None
    ),
    caption='Before and After'
)
print("✅ Demo data created!")
exit()
```

### 5. Start Backend Server

```bash
python manage.py runserver 0.0.0.0:8000
```

Backend is now at **http://localhost:8000**

### 6. Start Frontend Server

In a new terminal:

```bash
cd frontend
npm start
```

Frontend is now at **http://localhost:1234**

## 🔐 Firebase Authentication Flow

The app uses a secure two-step auth flow:

1. **User signs in with Firebase** (email/password via React)
2. **React gets Firebase ID token** and exchanges it with Django
3. **Django verifies token** with Firebase Admin SDK and issues a DRF token
4. **React stores DRF token** and uses it for all API calls

```
React Login → Firebase Auth → Get ID Token → POST /api/exchange-firebase-token/ → Get DRF Token → Use for API calls
```

## 📚 API Endpoints

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/users/` | GET | Token | List users |
| `/api/experts/` | GET | None | List experts (public) |
| `/api/portfolio-images/` | POST | Token | Upload portfolio image (experts only) |
| `/api/register/` | POST | None | Register new user |
| `/api/exchange-firebase-token/` | POST | None | Exchange Firebase ID token for DRF token |
| `/api/revoke-firebase-tokens/` | POST | Token | Revoke Firebase refresh tokens (admin) |
| `/admin/` | - | Admin | Django admin panel |

## 🧪 Running Tests

```bash
source .venv/bin/activate
export DJANGO_SETTINGS_MODULE=beauty.settings
pytest tests/ -v
```

Expected output: **5 tests passed**

- Firebase backend authentication
- Firebase token exchange
- Portfolio image upload
- User registration
- All other integration tests

## 🐳 Using Docker

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Place Firebase service account JSON at `./secrets/firebase-sa.json`

2. Build and start:

```bash
docker-compose up --build
```

3. Run migrations inside container:

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

4. Access:
   - Backend: http://localhost:8000
   - Admin: http://localhost:8000/admin
   - Postgres runs on localhost:5432 (credentials in docker-compose.yml)

### Validate Firebase Credentials

```bash
docker-compose exec web python manage.py validate_firebase_sa --file /run/secrets/firebase-sa.json --list-users
```

## 🌍 Production Deployment

### Environment Variables Required

```env
DJANGO_SECRET_KEY=<50+ char random string>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@db-host:5432/beauty
FIREBASE_ADMIN_CREDENTIAL=/path/to/service-account.json
```

### Security Hardening

The app automatically enables production security when `DJANGO_DEBUG=False`:

- ✅ HTTPS redirect
- ✅ Secure cookies (HttpOnly, Secure flags)
- ✅ HSTS headers (1 year max-age)
- ✅ CSP headers
- ✅ CSRF protection
- ✅ X-Frame-Options deny

### Recommended Hosting Options

1. **Google Cloud Run** (easiest for Django)
   ```bash
   gcloud run deploy beauty --source .
   ```

2. **AWS Elastic Beanstalk**
   ```bash
   eb create beauty-env
   ```

3. **DigitalOcean App Platform**
   - Connect GitHub repo
   - Set environment variables
   - Deploy

4. **Heroku** (read-only file system; use S3 for media)
   ```bash
   git push heroku main
   ```

### Media Storage (Production)

For production, configure S3:

```python
# In settings.py (production)
if not DEBUG:
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
            'OPTIONS': {
                'AWS_STORAGE_BUCKET_NAME': 'your-bucket',
                'AWS_S3_REGION_NAME': 'us-east-1',
            }
        }
    }
```

Then install: `pip install boto3 django-storages`

## 📖 Documentation

- [README.md](README.md) — Full project documentation
- [DEVELOPMENT.md](DEVELOPMENT.md) — Technical details
- [Firebase Setup](README.md#firebase-admin-backend) — Service account config

## 🆘 Troubleshooting

### Frontend can't reach backend
- Ensure backend is running on `0.0.0.0:8000` (not just `127.0.0.1`)
- Check `ALLOWED_HOSTS` includes your frontend origin
- Look for CORS errors in browser console (may need to add `django-cors-headers`)

### Firebase token verification fails
- Ensure `FIREBASE_ADMIN_CREDENTIAL` is set and valid
- Run: `python manage.py validate_firebase_sa --file ./secrets/firebase-sa.json`
- Check Firebase console that your app is registered

### Tests fail
- Ensure `DJANGO_SETTINGS_MODULE=beauty.settings` is exported
- Run `python manage.py migrate --noinput` first
- Check that all dependencies are installed: `pip install -r requirements.txt`

### Static files not loading
- Run: `python manage.py collectstatic --noinput` (production)
- In development, `DEBUG=True` serves them automatically

## 🎯 Next Steps

1. **Customize styling** — Edit `frontend/src/styles.css` and `templates/base.html`
2. **Add booking flow** — Extend `appointments` app with calendar UI
3. **Implement reviews** — Complete the `reviews` app with ratings
4. **Real-time chat** — Wire Channels WebSocket consumer to frontend
5. **Deploy to cloud** — Follow production deployment section above

## 📞 Support

For issues, check:
- GitHub Issues: https://github.com/willtalbot80/freelanceBeautyServices/issues
- Firebase Docs: https://firebase.google.com/docs
- Django DRF: https://www.django-rest-framework.org
- React Docs: https://react.dev

---

**Happy building!** 🎨✨
