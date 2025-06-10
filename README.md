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

#### Docker, able to create images and launch containers
 
#### Git
 - repo to clone from
   https://github.com/jsrmalvarez/workshop_crud_mcp
 
#### github account. This should give free accesst to copilot.
 
#### VSCode (updated)

#### VSCode extensions (see identifier for unambiguous identification)
 
##### Git
  - Git: vscode.git

##### Github Copilot
  - Github Copilot: github.copilot
  - Github Copilot Chat: github.copilot-chat  
 
##### Docker
  - Container Tools: ms-azuretools.vscode-containers

##### PlantUML
  - PlantUML jebbs.plantuml  
  - PlantUMLSyntax qhoekman.language-plantuml
  
Just if you want to check the code with syntax highlighting,
as the app runs containerized:

##### Backend  
  - Python: ms-python.python

##### Frontend  
  - TypeScript and Javascript Language Features: vscode.typescript-language-features  


## Environment Configuration

Create a `.env` file under the docker directory with the following content:

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