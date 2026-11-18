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

The ECR workflow publishes `healthcare-backend` and `healthcare-frontend` to Amazon ECR on pushes to `main` and version tags such as `v1.0.0`. The `main` branch also updates the `latest` tag. The Docker Hub workflow is paused for automatic events and remains available only through manual dispatch.

Before running the ECR workflow:

1. Create ECR repositories named `healthcare-backend` and `healthcare-frontend` in your AWS region.
2. Configure an AWS IAM OIDC provider for GitHub Actions and a role trusted by this GitHub repository's `main` branch. Grant it permission to push images to those ECR repositories.
3. Add these repository variables under **GitHub Settings → Secrets and variables → Actions → Variables**:
	- `AWSREGION`: the AWS region containing the ECR repositories.
	- `AWS_ACCOUNT_ID`: the 12-digit AWS account ID that owns the role.
	- `ASW_ROLE_1`: the IAM role name only, without an ARN or `role/` prefix.

No long-lived AWS access key is stored in GitHub; the workflow assumes the IAM role using OIDC. Compose image references use `AWS_ACCOUNT_ID`, `AWS_REGION`, and `IMAGE_TAG`. For local builds, run `docker compose up --build`; for pulling ECR images, set those variables and authenticate Docker to ECR first.

The tenant is identified by the `X-Tenant` header. Supported values are `tenant-a` and `tenant-b`. Tenant metadata is in the central database; patient records are stored in separate Tenant A and Tenant B databases.
