# Multi-Tenant Healthcare POC

A simple React + Django REST application demonstrating tenant isolation with separate PostgreSQL databases.

## Local development

Backend:

```powershell
cd backend
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py migrate --database=tenant_a
python manage.py migrate --database=tenant_b
python manage.py runserver
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite. The API runs at `http://localhost:8000/api`.

## Docker deployment

```powershell
docker compose up --build
```

Open `http://localhost:8080`.

The tenant is identified by the `X-Tenant` header. Supported values are `tenant-a` and `tenant-b`. Tenant metadata is in the central database; patient records are stored in separate Tenant A and Tenant B databases.
