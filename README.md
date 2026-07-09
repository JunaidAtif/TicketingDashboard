# Support Ticket Dashboard

A full-stack, Jira-style support ticket dashboard built with React (Frontend) and FastAPI (Backend).

## Features
- **Kanban Board**: Drag-and-drop support tickets across statuses (Open, In Progress, Resolved).
- **Authentication**: JWT-based secure login flow for agents.
- **Real-time Search & Filtering**: Filter tickets by status, priority, or search by title/customer name.
- **RESTful API**: Clean, documented FastAPI backend with data validation using Pydantic.

---

## 🛠️ Tech Stack

**Frontend:**
- React (with Vite)
- TypeScript
- Axios (API Client)
- @hello-pangea/dnd (Drag and Drop)
- Vanilla CSS with modern Glassmorphism UI

**Backend:**
- FastAPI (Python)
- SQLite (Database)
- SQLAlchemy (ORM)
- Pydantic (Validation schemas)
- python-jose & passlib (JWT Authentication)

---

## 🚀 Setup Instructions

### 1. Backend Setup

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
pip install fastapi "uvicorn[standard]" sqlalchemy pydantic python-jose passlib python-multipart "bcrypt==3.2.2" pytest
```

Seed the database with a default agent user (for testing):
```bash
python seed_db.py
```

Start the FastAPI development server:
```bash
uvicorn app.main:app --reload --port 8000
```
*The backend API will be running at `http://localhost:8000`.*
*The auto-generated API docs (Swagger UI) can be viewed at `http://localhost:8000/docs`.*

---

### 2. Frontend Setup

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

---

## 🔑 Default Login Credentials

Since the application is protected by JWT authentication, you will need to log in to view the dashboard. Use the following credentials created by the database seed script:

- **Username**: `agent`
- **Password**: `password123`

---

## 🧪 Running Tests

The backend includes a suite of automated tests using `pytest` to ensure data validation, authentication, and endpoints work correctly.

To run the backend tests:
```bash
cd backend
source venv/bin/activate
export PYTHONPATH=. 
pytest tests/ -v
```
