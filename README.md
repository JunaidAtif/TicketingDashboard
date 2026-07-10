# Support Ticket Dashboard

A full-stack, Jira-style support ticket management system designed for customer support teams. Built with a modern React frontend and a highly scalable FastAPI backend.

**Live Demo:** [https://ticketingdashboard-lj2r5x2h8-tommyreirdon.vercel.app/](https://ticketingdashboard-lj2r5x2h8-tommyreirdon.vercel.app/)

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

## Future Improvements (If there were more time)
While the core system is robust, there are several enhancements that would elevate this project to an enterprise level:

1. **Real-time Updates (WebSockets)**: Currently, if two agents are looking at the Kanban board, they won't see each other moving tickets. Implementing WebSockets in FastAPI would allow real-time syncing across all clients.
2. **Frontend Testing**: Introduce `Jest` and `React Testing Library` for unit testing hooks/components, and `Playwright` for End-to-End user flow testing.
3. **CI/CD Pipelines**: Add GitHub Actions workflows to automatically run linters (`flake8`, `eslint`), test suites, and deploy to staging environments on every pull request.
4. **Pagination & Caching**: As the ticket volume grows into the tens of thousands, the `GET /tickets` endpoint would need cursor-based pagination and potentially a Redis caching layer to maintain performance.
5. **Role-Based Access Control (RBAC)**: Expand the simple JWT auth into a full RBAC system, distinguishing between `Agents` (who resolve tickets) and `Admins` (who manage the agents and system settings).
