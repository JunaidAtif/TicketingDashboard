import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api.v1 import auth, tickets

app = FastAPI(title="Support Ticket Dashboard API")

# Configure CORS - driven entirely by environment variables
# In production, set FRONTEND_URL to your deployed frontend domain
# When FRONTEND_URL is not set (local dev), all origins are allowed
frontend_url = os.environ.get("FRONTEND_URL", "")

allowed_origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://localhost:3000",
]

if frontend_url:
    allowed_origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if frontend_url else ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = str(error["loc"][-1])
        message = error["msg"]
        errors.append({"field": field, "message": message, "type": error["type"]})
    
    return JSONResponse(
        status_code=422,
        content={"errors": errors}
    )

app.include_router(auth.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Support Ticket API"}
