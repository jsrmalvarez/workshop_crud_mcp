from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import items
from app.core.database import engine
from app.models import models

app = FastAPI(
    title="CRUD API",
    description="A CRUD API with FastAPI and SQLAlchemy",
    version="1.0.0"
)

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(items.router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    models.Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up database connections on shutdown."""
    # If using a connection pool or need to close anything explicitly, do it here
    pass

@app.get("/")
def read_root():
    return {"message": "Welcome to the CRUD API"}