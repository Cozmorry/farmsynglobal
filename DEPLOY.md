# Deploy FarmSyn Global on Render

## Overview

- **Backend**: Python Web Service (FastAPI) at `farmsyn-api` (or your chosen name).
- **Frontend**: Static Site (Vite/React) at `farmsyn-web`.
- **Database**: Use an external MySQL (e.g. [PlanetScale](https://planetscale.com), [Railway](https://railway.app), or any MySQL host). Render does not offer MySQL; you can use Render Postgres only if you switch the app to PostgreSQL.

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
| `DATABASE_URL`  | Your MySQL URL, e.g. `mysql+pymysql://USER:PASSWORD@HOST:3306/DATABASE`. |
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

## 5. MySQL

- Create a MySQL database with any provider (PlanetScale, Railway, etc.).
- Use a connection string in the form:  
  `mysql+pymysql://USER:PASSWORD@HOST:3306/DATABASE`
- Ensure the host allows connections from Render (e.g. allow 0.0.0.0/0 or Render’s IPs if documented).
- Put this string in the backend’s `DATABASE_URL` env var.

---

## 6. After deploy

- Backend: `https://<your-backend>.onrender.com` (e.g. `/health`, `/api/v1/...`).
- Frontend: `https://<your-frontend>.onrender.com`.
- Free-tier services spin down after inactivity; first request may be slow.
