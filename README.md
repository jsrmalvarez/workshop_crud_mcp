# Simple CRUD

A full-stack CRUD (Create, Read, Update, Delete) application with:
- Frontend: React with Chakra UI components
- Backend: Python FastAPI with SQLAlchemy ORM
- Database: MariaDB
- MCP Server: Model Context Protocol implementation

## Architecture

```
┌─────────────────┐             ┌─────────────────┐
│    Frontend     │             │    Database     │
│  (React + UI)   │             │(MariaDB/SQLite) │
└────────┬────────┘             └────────▲────────┘
         │                               │
         │                               │
         ▼                               │
┌─────────────────┐                      │
│    Backend      │                      │
│   (FastAPI)     │──────────────────────┘
└────────┬────────┘
         ▲
         │
┌────────┴────────┐
│   MCP Server    │
│  (FastAPI MCP)  │
└────────▲────────┘
         │
         │
┌────────┴─────────┐         ┌─────────────────┐
│   MCP Client     │────────►│      LLM        │
│ (Github Copilot) │         │                 │
└──────────────────┘         └─────────────────┘

```

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

## Environment Configuration

Create a `.env` file in the backend directory with the following content:

```env
ENVIRONMENT=development  # or production
```

When `ENVIRONMENT` is set to `development`, the application will use an in-memory SQLite database for faster development and testing. In `production` mode, it will use the configured MariaDB database.

## Running with Docker

1. Start all services using Docker Compose:

```bash
cd docker
docker-compose up --build -d
```

This will start three containers:
- MariaDB database on port 3306
- Backend API on port 8000
- Frontend React app on port 3000

2. Access the application at http://localhost:3000

## API Endpoints

- `GET /api/items/`: List all items
- `POST /api/items/`: Create new item (C)
- `POST /api/items/batch`: Create multiple items in a single request
- `GET /api/items/{id}`: Get a specific item (R)
- `PUT /api/items/{id}`: Update a specific item (U)
- `DELETE /api/items/{id}`: Delete a specific item (D)
- `DELETE /api/items/batch`: Delete multiple items in a single request