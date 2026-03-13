# Deploy FarmSyn Global on Render

## Overview

- **Backend**: Python Web Service (FastAPI) at `farmsyn-api` (or your chosen name).
- **Frontend**: Static Site (Vite/React) at `farmsyn-web`.
- **Database**: **PostgreSQL**. Use [Render Postgres](https://render.com/docs/databases) (same dashboard) or any Postgres host.

---

## Local development (PostgreSQL)

For local testing you need a running Postgres server.

**Option 1 – Install PostgreSQL locally**

- **Windows**: [PostgreSQL installer](https://www.postgresql.org/download/windows/)
- **macOS**: `brew install postgresql@16` then `brew services start postgresql@16`
- **Linux**: `sudo apt install postgresql` (or your distro’s package)

Then create a database and user:

```bash
# In psql or pgAdmin: create database and (optionally) a user
CREATE DATABASE farmsyn;
# If you use a dedicated user:
# CREATE USER farmsyn_user WITH PASSWORD 'yourpassword';
# GRANT ALL PRIVILEGES ON DATABASE farmsyn TO farmsyn_user;
```

In `.env` set:

```env
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/farmsyn
```

**Option 2 – Postgres in Docker (no full install)**

```bash
docker run -d --name postgres-farmsyn -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=farmsyn -p 5432:5432 postgres:16
```

Then:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/farmsyn
```

**Option 3 – Hosted Postgres**

Use a free tier (e.g. [Neon](https://neon.tech), [Supabase](https://supabase.com), or Render Postgres) and put the connection string in `DATABASE_URL`.

---

## 1. Prepare the repo

- Push the project to GitHub (or GitLab).
- Ensure `requirements.txt` and `render.yaml` are in the repo root.

---

## 2. Create services on Render

### Option A: Blueprint (recommended)

1. Go to [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**.
2. Connect your repo and select the repo that contains `render.yaml`.
3. Render will detect `render.yaml` and create both services.
4. For each service, set the **environment variables** (see below).

### Option B: Manual

**Backend (Web Service)**

1. **New** → **Web Service**.
2. Connect the repo, set:
   - **Root Directory**: leave empty (repo root).
   - **Runtime**: Python.
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
3. Add environment variables (see below).

**Frontend (Static Site)**

1. **New** → **Static Site**.
2. Connect the same repo, set:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
3. Add `VITE_API_BASE_URL` (see below).

---

## 3. Environment variables

### Backend (`farmsyn-api`)

| Key             | Value / action |
|-----------------|----------------|
| `ENV`           | `production` (optional; Blueprint sets it.) |
| `SECRET_KEY`    | Long random string (or use “Generate” in Render). |
| `DATABASE_URL`  | PostgreSQL URL, e.g. `postgresql+psycopg2://USER:PASSWORD@HOST:5432/DATABASE`. On Render you can link a Postgres DB and use **Secret Files** or the DB’s **Internal Connection String**. |
| `FRONTEND_URLS` | Comma-separated frontend origins for CORS, e.g. `https://farmsyn-web.onrender.com`. |

### Frontend (`farmsyn-web`)

| Key                  | Value |
|----------------------|--------|
| `VITE_API_BASE_URL`  | Backend URL with no trailing slash, e.g. `https://farmsyn-api.onrender.com`. |

Important: set `VITE_API_BASE_URL` **before** the first build; Vite bakes it in at build time.

---

## 4. Order of setup

1. Create and deploy the **backend** first.
2. Copy the backend URL (e.g. `https://farmsyn-api.onrender.com`).
3. In the **frontend** service, set `VITE_API_BASE_URL` to that URL and (re)deploy.
4. In the **backend**, set `FRONTEND_URLS` to your frontend URL (e.g. `https://farmsyn-web.onrender.com`) and redeploy if needed.

---

## 5. PostgreSQL on Render

1. In the Render dashboard: **New** → **PostgreSQL**.
2. Create the database (e.g. name `farmsyn`).
3. In the DB’s **Info** tab, copy the **Internal Database URL** (or External if your backend is not on Render).
4. In your **backend** service, set `DATABASE_URL` to that URL (Render can inject it via **Connect** when you add the database to the same Blueprint).

---

## 6. After deploy

- Backend: `https://<your-backend>.onrender.com` (e.g. `/health`, `/api/v1/...`).
- Frontend: `https://<your-frontend>.onrender.com`.
- Free-tier services spin down after inactivity; first request may be slow.
