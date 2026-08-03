# Camp Security

Full-stack security company website with a **Next.js** frontend, **Django REST API** backend, and **PostgreSQL** database.

| | |
|---|---|
| **Live demo (frontend)** | [https://camp-security.vercel.app](https://camp-security.vercel.app) *(deploy to activate)* |
| **API (backend)** | [https://camp-api.onrender.com/api](https://camp-api.onrender.com/api) *(deploy to activate)* |
| **License** | [MIT](LICENSE) |

> Replace the demo URLs above with your actual Vercel and Render/Railway deployment links after publishing.

---

## Problem This Solves

Small and mid-size security firms often rely on static brochure sites with no way to capture leads, update services, or manage content without editing HTML. **Camp Security** demonstrates a production-style solution: a decoupled frontend for fast UX, a REST API for structured content, PostgreSQL for persistence, and a contact form that stores inquiries in the database (viewable in Django admin).

---

## What I Built

| Layer | What I implemented |
|---|---|
| **Frontend** | Next.js 15 App Router, Tailwind CSS, responsive dark theme, 6 pages, contact form with API integration |
| **Backend** | Django 5 + DRF, REST endpoints for services/industries/jobs/site content, contact inquiry POST endpoint |
| **Database** | PostgreSQL models for services, industries, job openings, and contact inquiries |
| **DevOps** | Docker Compose for local Postgres, Render blueprint, Vercel config, environment-based settings |
| **Quality** | API test suite, seed command, `.gitignore`, MIT license |

---

## Tech Stack

| Category | Technology |
|---|---|
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS |
| Backend | Django 5, Django REST Framework |
| Database | PostgreSQL 16 |
| Deployment | Vercel (frontend) + Render / Railway / Fly.io (backend) |
| Tooling | Docker Compose, Gunicorn, WhiteNoise |

---

## Features

- **Home** — hero section with featured services from the API
- **About** — mission, certifications, and team overview
- **Services** — full service catalog loaded from PostgreSQL
- **Clients** — industries served + testimonial
- **Careers** — open roles and benefits from the API
- **Contact** — contact details + working inquiry form (saved to DB)
- **Admin** — Django admin for content and inquiry management
- **Health check** — `GET /api/health/` for deployment monitoring

---

## Screenshots

| Home | Services | Contact |
|:---:|:---:|:---:|
| ![Home page](docs/screenshots/home.svg) | ![Services page](docs/screenshots/services.svg) | ![Contact page](docs/screenshots/contact.svg) |

After running locally, replace these with real PNG captures:

```bash
# Example: capture from localhost:3000 and save to docs/screenshots/
```

---

## Project Structure

```
camp/
├── backend/          # Django REST API
│   ├── camp/         # Project settings
│   ├── core/         # Models, serializers, views, tests
│   ├── manage.py
│   ├── requirements.txt
│   └── render.yaml   # Render deployment blueprint
├── frontend/         # Next.js + Tailwind
│   └── src/
│       ├── app/      # Pages (App Router)
│       ├── components/
│       └── lib/      # API client
├── docs/screenshots/
├── docker-compose.yml
├── LICENSE
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker (for PostgreSQL) or a local Postgres instance

### 1. Clone and start PostgreSQL

```bash
git clone <your-repo-url>
cd camp
docker compose up -d
```

### 2. Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

API runs at **http://localhost:8000/api/**

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Frontend runs at **http://localhost:3000**

### Windows notes

- Use `copy .env.example .env` instead of `cp` in Command Prompt.
- Do **not** paste lines starting with `#` — CMD treats them as commands.
- If port 5432 is already in use (common with a local PostgreSQL install), this project uses **5433** for Docker Postgres.

### Troubleshooting: database connection failed

If you see `password authentication failed for user "camp"`:

1. Another PostgreSQL may be running on port 5432. This project maps Docker to **5433**.
2. Recreate the container:

```bash
docker compose down
docker compose up -d
```

3. Confirm the port mapping shows `0.0.0.0:5433->5432/tcp`:

```bash
docker ps
```

4. Ensure `backend/.env` has:

```
DATABASE_URL=postgres://camp:camp@localhost:5433/camp
```

---

## Environment Variables

### Backend (`backend/.env`)

| Variable | Description | Example |
|---|---|---|
| `SECRET_KEY` | Django secret key | `your-random-secret` |
| `DEBUG` | Debug mode | `True` (dev) / `False` (prod) |
| `ALLOWED_HOSTS` | Comma-separated hosts | `localhost,127.0.0.1,your-api.onrender.com` |
| `DATABASE_URL` | PostgreSQL connection URL | `postgres://camp:camp@localhost:5433/camp` |
| `CORS_ALLOWED_ORIGINS` | Frontend origins | `http://localhost:3000,https://your-app.vercel.app` |
| `CONTACT_EMAIL` | Info email shown on site | `info@campsecurity.com` |
| `SALES_EMAIL` | Sales email | `sales@campsecurity.com` |
| `CAREERS_EMAIL` | Careers email | `careers@campsecurity.com` |

### Frontend (`frontend/.env.local`)

| Variable | Description | Example |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000/api` |

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health/` | Health check |
| `GET` | `/api/site/` | Aggregated page content + contact info |
| `GET` | `/api/services/` | All services |
| `GET` | `/api/industries/` | Client industries |
| `GET` | `/api/jobs/` | Open job roles |
| `POST` | `/api/contact/` | Submit contact inquiry |

---

## Running Tests

```bash
cd backend
python manage.py test core
```

Tests use an in-memory SQLite database so Postgres does not need to be running.

---

## Deployment

### Frontend → Vercel

1. Import the repo in [Vercel](https://vercel.com)
2. Set root directory to `frontend`
3. Add env var: `NEXT_PUBLIC_API_URL=https://your-api.onrender.com/api`
4. Deploy

### Backend → Render

1. Connect repo in [Render](https://render.com)
2. Use `backend/render.yaml` blueprint, or create a **Web Service**:
   - **Root directory:** `backend`
   - **Build:** `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_data`
   - **Start:** `gunicorn camp.wsgi --bind 0.0.0.0:$PORT`
3. Attach a PostgreSQL database and set `DATABASE_URL`, `SECRET_KEY`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`

### Backend → Railway / Fly.io

Same build/start commands as Render. Set the same environment variables from `backend/.env.example`.

---

## License

MIT — see [LICENSE](LICENSE).
