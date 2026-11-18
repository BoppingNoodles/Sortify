
# Sortify Backend Deployment Guide

## 1. Overview

The Sortify backend is a FastAPI application packaged using a multi-stage Dockerfile.

It can be deployed as a publicly accessible HTTPS service using Render or Google Cloud Run.

The application exposes a health-check endpoint at `/health`.

## 2. Docker Configuration

The Dockerfile is located at:

`backend/Dockerfile`

The Docker build context must be the repository root because the requirements file is located at the root.
Keep local credentials outside the repository and provide them at runtime.
Pass `--env-file /path/to/local.env` to `docker run` to supply local environment variables.

Build the image:

```bash
docker build -f backend/Dockerfile -t sortify-backend .
```

Run locally:

```bash
docker run --rm -p 8000:8000 sortify-backend
```

Verify the health endpoint:

```bash
curl -i http://localhost:8000/health
```

Expected response:

```json
{"status": "ok"}
```

## 3. Render Deployment

1. Push the deployment branch to GitHub.
2. Open https://dashboard.render.com/.
3. Create a new Web Service.
4. Connect the Sortify GitHub repository.
5. Select the deployment branch or `main` after the changes are merged.
6. Select Docker as the runtime.
7. Set the Dockerfile path to `backend/Dockerfile`.
8. Set the Docker build context to the repository root.
9. Deploy the service.

The Dockerfile uses the `PORT` environment variable and binds Uvicorn to `0.0.0.0`.

## 4. Environment Variables

Configure the following environment variables in Render:

| Variable | Value |
|---|---|
| `PORT` | `8000` (if configuring the service to use port 8000) |
| `PROJECT_NAME` | `Sortify API` |
| `ENV` | `production` |
| `CORS_ORIGINS` | JSON array of deployed frontend origins |

Example CORS configuration:

```text
["https://your-frontend-domain.com"]
```

Replace the example URL with the actual deployed frontend origin.

Do not use a wildcard origin when credentialed CORS requests are required.

Additional variables may be required depending on the selected authentication, database, and storage configuration.

## 5. Health Check Verification

After deployment, locate the public HTTPS URL provided by Render.

Run:

```bash
curl -i https://YOUR-SERVICE-URL/health
```

Expected HTTP status:

```text
HTTP/2 200
```

Expected response body:

```json
{"status": "ok"}
```

A successful response confirms that the public backend service is responding.

## 6. Production Notes

- Keep service credentials and private keys out of Git.
- Configure production CORS origins explicitly.
- When Firebase uses a service account file, add `serviceAccountKey.json` as a Render
  Secret File and set `FIREBASE_CREDENTIALS_PATH=/etc/secrets/serviceAccountKey.json`.
  For local Docker runs, mount the file read-only from outside the build context
  and set `FIREBASE_CREDENTIALS_PATH` to its container path.
- Monitor deployment logs for startup errors.
- Verify the health endpoint after every production deployment.
