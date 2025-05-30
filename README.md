# Simple CRUD

A full-stack CRUD (Create, Read, Update, Delete) application with:
- Frontend: React with Chakra UI components
- Backend: Python FastAPI with SQLAlchemy ORM
- Database: MariaDB

## Project Structure

```
.
├── backend/               # Python FastAPI backend
│   ├── app/               # Application code
│   │   ├── core/          # Core functionality
│   │   ├── models/        # SQLAlchemy models
│   │   ├── routers/       # API endpoints
│   │   └── schemas/       # Pydantic schemas

├── frontend/              # React frontend
│   ├── public/            # Public assets
│   └── src/               # React source code
│       └── components/    # React components
└── docker/                # Docker configuration
    ├── docker-compose.yml # Docker compose config
    ├── backend.Dockerfile # Backend Docker config
    └── frontend.Dockerfile # Frontend Docker config
```

## Prerequisites

- Docker and Docker Compose

## Running with Docker

1. Start all services using Docker Compose:

```bash
cd docker
docker-compose up
```

This will start three containers:
- MariaDB database on port 3306
- Backend API on port 8000
- Frontend React app on port 3000

2. Access the application at http://localhost:3000

## API Endpoints

- `GET /api/items/`: List all items
- `POST /api/items/`: Create new item (C)
- `GET /api/items/{id}`: Get a specific item (R)
- `PUT /api/items/{id}`: Update a specific item (U)
- `DELETE /api/items/{id}`: Delete a specific item (D)