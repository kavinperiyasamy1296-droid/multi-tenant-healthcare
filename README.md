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

## Publish images with GitHub Actions

Create Docker Hub repositories named `healthcare-backend` and `healthcare-frontend` under your account. In the GitHub repository, add these Actions repository secrets under **Settings → Secrets and variables → Actions**:

- `DOCKERHUB_TOKEN`: a Docker Hub access token

The workflow builds both images for pull requests without publishing. Pushes to `main` and version tags such as `v1.0.0` publish images to Docker Hub. The `main` branch also updates the `latest` tag. After publishing, Compose uses `DOCKERHUB_USERNAME/healthcare-backend` and `DOCKERHUB_USERNAME/healthcare-frontend`; set `DOCKERHUB_USERNAME` in the shell if the account differs from the default in `docker-compose.yml`.

The tenant is identified by the `X-Tenant` header. Supported values are `tenant-a` and `tenant-b`. Tenant metadata is in the central database; patient records are stored in separate Tenant A and Tenant B databases.
