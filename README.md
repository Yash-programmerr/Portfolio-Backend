# Portfolio Backend (FastAPI + MongoDB Atlas)

## Setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
uvicorn app.main:app --reload --port 8000
```

First start seeds the admin user from `ADMIN_EMAIL` / `ADMIN_PASSWORD` in `.env` if the users collection is empty.

## Seed content

To migrate the current hardcoded portfolio content into Mongo:

```powershell
python -m scripts.seed
```

Idempotent — safe to re-run; uses upserts on stable keys.

## API

- `POST /api/auth/login` — `{email, password}` → `{access_token, token_type}`
- `GET  /api/auth/me` — requires Bearer token
- `GET  /api/hero`           `PUT /api/hero`          (singleton)
- `GET  /api/about`          `PUT /api/about`         (singleton)
- `GET  /api/skills`         `POST/PUT/DELETE /api/skills[/{id}]`
- `GET  /api/projects`       `POST/PUT/DELETE /api/projects[/{id}]`
- `GET  /api/achievements`   `POST/PUT/DELETE /api/achievements[/{id}]`
- `GET  /api/social-links`   `POST/PUT/DELETE /api/social-links[/{id}]`
- `GET  /api/resume`         `PUT /api/resume`        (singleton)

All mutating routes require `Authorization: Bearer <token>`.

## Production deployment notes

Before deploying anywhere (Render, Railway, Fly, Docker, etc.):

1. **Generate a fresh `JWT_SECRET`** — never reuse the dev one.
   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(48))"
   ```
   Paste the output into the host's environment variable settings as `JWT_SECRET`.
   **Do NOT commit it to git.**

2. **Set the other env vars on the host:**
   - `MONGODB_URI` — production Atlas connection string (ideally a separate DB user with access only to the portfolio DB)
   - `ADMIN_EMAIL` / `ADMIN_PASSWORD` — credentials for the seed-on-first-boot admin
   - `CORS_ORIGINS` — comma-separated list of allowed frontend domains (e.g. `https://yashverma.dev,https://www.yashverma.dev`)
   - `JWT_EXPIRE_MINUTES` — how long admin tokens stay valid (default 720 = 12h)

3. **Verify `.env` is in `.gitignore`** — already configured.

4. **Rotating the secret** invalidates every existing JWT — you (and any other admin sessions) will need to re-login.

