# URL Shortener
A clean, modular FastAPI application for shortening URLs using TinyURL. Built with a DDD-inspired architecture, 
type-checked interfaces, and layered separation of concerns.
## Features
- FastAPI-based REST API with async support
- Two main endpoints:
  - POST /: Saves original and shortened URLs to DB
    - Returns 201 Created if new URL added
    - Returns 200 OK if URL already exists
  - GET /{id}: Redirects to the original URL via 307 Temporary Redirect
- TinyURL service integration
- PostgreSQL as the primary database
- PGAdmin available for DB inspection
- Pydantic models for request/response bodies
- Domain-Driven Design (DDD) layout
- Dockerized for consistent environments
- Tested with Pytest (74% coverage)
## Project Structure
```
.                                           # Project root
├── src/                                    # Application source code
│   └── shortener_app/                      # Domain-specific application logic
│       ├── main.py                         # Application entrypoint
│       ├── config.py                       # Configuration management
│       ├── asyncclient.py                  # Async HTTP client for demonstration purposes
│       ├── domain/                         # Domain layer: core models and business logic, independent of frameworks
│       │   ├── models.py                   # Pure Python model class, decoupled from ORM
│       │   ├── services.py                 # Encapsulates logic for creating shortened URLs
│       │   ├── errors.py                   # Custom exceptions translating infra errors to domain-level
│       │   └── protocols.py                # Interfaces for repository, session and unit of work
│       ├── application/                    # Business orchestration and Unit of Work pattern
│       │   ├── app_manager.py              # High-level operations over domain + persistence
│       │   └── unit_of_work.py             # Unit of Work pattern implementation
│       ├── entrypoints/                    # Interfaces to trigger business logic (e.g. API, CLI, bot)
│       │   └── fastapi_app/                # HTTP interface via FastAPI
│       │       ├── routes/                 # HTTP route definitions
│       │       │   ├── healthcheck.py      # Health check endpoint
│       │       │   └── shortener.py        # Endpoints for URL shortening logic
│       │       ├── __init__.py             # Initializes and configures the main FastAPI router
│       │       ├── init_app.py             # Creates FastAPI app with preconfigured routes and middleware
│       │       ├── run_app.py              # Launch script for FastAPI server
│       │       └── schemas.py              # Pydantic models defining request and response bodies
│       └── infrastructure/                 # Infrastructure layer
│           ├── orm_tool/                   # ORM setup and database session handling
│           │   ├── init_orm_tool.py        # Initializes ORM tool (e.g. SQLAlchemy)
│           │   └── sql_alchemy_wrapper.py  # SQLAlchemy setup and support functions
│           ├── drop_create_tables.py       # Database table drop-create script
│           └── repository/                 # Repository implementation using ORM tool instance
├── tests/                                  # Test suite (pytest-based)
├── docker-compose.yml                      # Production Docker Compose definition
├── Dockerfile                              # Docker image definition
├── Makefile                                # Build, run, and test automation
├── requirements.txt                        # Runtime dependencies
├── requirements-dev.txt                    # Dev and test dependencies
└── pytest.ini                              # Pytest configuration
```
## API Overview
The API provides two endpoints:
1. `POST /`

    Creates a shortened URL.
   - If the original URL is new, returns:
     - 201 Created
     - JSON: { "id": 123, "short_url": "http://..." }

   - If the original URL already exists in the database, returns:
     - 200 OK
     - JSON: { "id": 123, "short_url": "http://..." }



2. `GET /{id}`

    Redirects to the original URL associated with the given ID.
    - returns: 307 Temporary Redirect
    - redirects to the original URL

## Running the App
### Build containers (dev / prod / test):
```bash
$ make build MODE=prod   # or dev / test
```
### Run app (dev / prod / test):
```bash
$ make run MODE=prod   # FastAPI app + database + asyncclient + PGAdmin
```
### Run tests:
```bash
$ make test
```
### Async client:
In dev and prod modes, the app launches an internal asyncclient.py module that sends demo HTTP requests to the API.
The responses are printed directly into the container logs:
```
prod_asyncclient      | (201, {'id': 1, 'short_url': 'https://tinyurl.com/yqp7ct'})
prod_asyncclient      | (200, {'original_url': 'https://example.com/'})
```
## Swagger UI
Once running, access the automatically generated Swagger UI at:
```bash
http://localhost:8080/docs
```