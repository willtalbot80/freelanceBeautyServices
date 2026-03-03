Frontend
--------

A minimal React frontend scaffold is available in `frontend/`. To run it:

```bash
cd frontend
npm install
npm start
```

The frontend uses Parcel and fetches the API at `/api/experts/` (assumes Django is running on same host).

CI / Tests
---------

A GitHub Actions workflow is in `.github/workflows/ci.yml` which installs dependencies, runs migrations, and executes tests with `pytest`.

Run tests locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest pytest-django pillow
python manage.py migrate
pytest
```
