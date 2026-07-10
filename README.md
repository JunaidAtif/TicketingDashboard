# Support Ticket Dashboard

A full-stack, Jira-style support ticket management system designed for customer support teams. Built with a modern React frontend and a highly scalable FastAPI backend.

---

## Key Features
- **Kanban Board & List Views**: Visually drag-and-drop tickets across statuses (Open, In Progress, Resolved) or view them in a traditional data list.
- **Real-time Search & Filtering**: Instantly search tickets by title or customer name across both views.
- **Authentication**: JWT-based secure login flow for agents.
- **RESTful API**: Clean, documented FastAPI backend with strict data validation using Pydantic.

---

## Architecture & Technical Choices

### Backend (Python / FastAPI)
The backend employs a **Layered Architecture** (Controller → Service → Repository → Database). 
- **Why?** While a flat structure is faster for prototyping, a layered approach completely decouples the database layer from the HTTP layer. This makes the codebase highly testable, modular, and easy to scale. If we were to switch ORMs tomorrow, the API routes wouldn't need to change.
- **Database**: We transitioned from SQLite to **PostgreSQL**. Postgres provides robust concurrency control, superior data integrity, and is production-ready.
- **Migrations**: Database schema changes are tracked and executed deterministically using **Alembic**.

### Frontend (React / Vite)
The frontend utilizes a **Feature-based Module Structure**. 
- **Why?** Grouping code by feature (e.g., `components/Ticket`, `components/Auth`) rather than by technical type keeps related code close together, significantly reducing cognitive load as the application grows.
- **State Management**: Complex state and data fetching are abstracted into custom React hooks (`useTickets`, `useAuth`), keeping UI components pure and focused on rendering.
- **Styling**: We opted for **Vanilla CSS** to implement a highly customized, premium "Glassmorphism" dark-mode aesthetic without being constrained by utility-class frameworks.

---

## Tech Stack

**Frontend:**
- React 18 (Bootstrapped with Vite)
- TypeScript
- Axios (API Client & Interceptors)
- `@hello-pangea/dnd` (Drag and Drop)
- Vanilla CSS 

**Backend:**
- FastAPI (Python)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Alembic (Migrations)
- Pydantic (Data Validation)
- `python-jose` & `passlib` (JWT Auth & Hashing)
- Pytest (Automated Testing)

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker & Docker Compose

### Quickstart (Docker Compose)
The fastest way to run the entire stack locally:
```bash
# 1. Copy and configure environment variables
cp backend/.env.example backend/.env

# 2. Start all services (database, backend, frontend)
docker compose up --build

# 3. Open the app
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# Swagger Docs: http://localhost:8000/docs
```

The Docker Compose setup automatically:
- Starts a PostgreSQL database
- Runs database migrations (`alembic upgrade head`)
- Seeds the default admin user
- Starts the FastAPI backend
- Builds and serves the React frontend via Nginx

### Manual Setup (Without Docker)

#### 1. Database Setup
Start only the PostgreSQL container in the background:
```bash
docker compose up db -d
```

### 2. Backend Setup
Open a terminal and navigate to the backend directory:
```bash
cd backend
```

Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the required Python dependencies:
```bash
pip install -r requirements.txt
```

Run database migrations to build the schema in Postgres:
```bash
export PYTHONPATH=. 
alembic upgrade head
```

Seed the database with a default agent user (for testing):
```bash
export PYTHONPATH=.
python scripts/seed_admin.py
```

Start the FastAPI development server:
```bash
uvicorn app.main:app --reload --port 8000
```
*The backend API will be running at `http://localhost:8000`.*
*The auto-generated API docs (Swagger UI) can be viewed at `http://localhost:8000/docs`.*

---

### 3. Frontend Setups
Open a new terminal window and navigate to the frontend directory:
```bash
cd frontend
```

Install the Node dependencies:
```bash
npm install
```

Start the Vite development server:
```bash
npm run dev
```
*The frontend application will be accessible at the URL shown in your terminal (usually `http://localhost:5173`).*

### 4. Open the App
Once everything is running, you can access the different parts of the application here:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

---

## Default Login Credentials
Since the application is protected by JWT authentication, you will need to log in to view the dashboard. Use the following credentials created by the database seed script:

- **Username**: `admin`
- **Password**: `password123`

*(Note: These default credentials can be customized via the `ADMIN_USERNAME` and `ADMIN_PASSWORD` variables in the `backend/.env` file).*

---

## Running Tests
The backend includes a suite of automated tests using `pytest` to ensure data validation, authentication, and endpoints work correctly.

To run the backend tests:
```bash
cd backend
source venv/bin/activate
export PYTHONPATH=. 
pytest tests/ -v
```

---

## Cloud Deployment

The application is designed to be deployed with the backend on **Railway** (or any container host) and the frontend on **Vercel** (or any static host). All configuration is driven by environment variables -- no URLs or secrets are hardcoded in the codebase.

### Backend (Railway)

Set the following environment variables in your Railway backend service:

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (reference from your Railway Postgres service) |
| `SECRET_KEY` | A long, random cryptographic key for signing JWT tokens |
| `ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` (24 hours) |
| `ADMIN_USERNAME` | Username for the initial admin account |
| `ADMIN_PASSWORD` | Password for the initial admin account |
| `FRONTEND_URL` | Your Vercel frontend URL (for CORS, e.g. `https://your-app.vercel.app`) |

Set the custom start command to:
```
alembic upgrade head && python -m scripts.seed_admin && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vercel)

Set the following environment variable in your Vercel project settings:

| Variable | Description |
|----------|-------------|
| `VITE_API_URL` | Your Railway backend URL with the API prefix (e.g. `https://your-backend.up.railway.app/api/v1`) |

After setting or changing `VITE_API_URL`, you must redeploy the frontend for the change to take effect (Vite bakes environment variables into the JavaScript bundle at build time).

---

## Future Improvements (If there were more time)
While the core system is robust, there are several enhancements that would elevate this project to an enterprise level:

1. **Real-time Updates (WebSockets)**: Currently, if two agents are looking at the Kanban board, they won't see each other moving tickets. Implementing WebSockets in FastAPI would allow real-time syncing across all clients.
2. **Frontend Testing**: Introduce `Jest` and `React Testing Library` for unit testing hooks/components, and `Playwright` for End-to-End user flow testing.
3. **CI/CD Pipelines**: Add GitHub Actions workflows to automatically run linters (`flake8`, `eslint`), test suites, and deploy to staging environments on every pull request.
4. **Pagination & Caching**: As the ticket volume grows into the tens of thousands, the `GET /tickets` endpoint would need cursor-based pagination and potentially a Redis caching layer to maintain performance.
5. **Role-Based Access Control (RBAC)**: Expand the simple JWT auth into a full RBAC system, distinguishing between `Agents` (who resolve tickets) and `Admins` (who manage the agents and system settings).
