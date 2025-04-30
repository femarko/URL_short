# URL Shortener
A modular and extensible URL shortener service built with FastAPI, SQLAlchemy, and Docker. This project follows Clean Architecture principles and is structured for scalability, testability, and maintainability.

## Project Structure
```
.                                      # Project root
├── src/                               # Application source code
│   ├── main.py                        # Application entrypoint
│   ├── config.py                      # Configuration management
│   ├── asyncclient.py                 # Async HTTP client for demonstration purposes
│   └── shortener_app/                 # Domain-specific application logic
│       ├── db/                        # Database table drop-create script
│       ├── domain/                    # Domain layer: core models and business logic, independent of frameworks
│       │   ├── models.py              # Pure Python model class, decoupled from ORM
│       │   ├── services.py            # Encapsulates logic for creating shortened URLs
│       │   ├── errors.py              # Custom exceptions translating infra errors to domain-level
│       │   └── protocols.py           # Interfaces for repository, session and unit of work
│       ├── entrypoints/               # Interfaces to trigger business logic (e.g. API, CLI, bot)
│       │   └── fastapi_app/           # HTTP interface via FastAPI
│       │       ├── init_app.py        # Creates FastAPI app with preconfigured routes and middleware
│       │       ├── routes/            # HTTP route definitions
│       │       │   ├── healthcheck.py # Health check endpoint
│       │       │   └── shortener.py   # Endpoints for URL shortening logic
│       │       ├── run_app.py         # Launch script for FastAPI server
│       │       └── schemas.py         # Pydantic models defining request and response bodies
│       ├── orm_tool/                  # Infrastructure layer: ORM setup and database session handling
│       │   ├── init_orm_tool.py       # Initializes ORM tool (e.g. SQLAlchemy)
│       │   └── sql_alchemy_wrapper.py # SQLAlchemy setup and support functions
│       ├── repository/                # Repository implementations using SQLAlchemy
│       └── service_layer/             # Business orchestration and Unit of Work pattern
│           ├── app_manager.py         # High-level operations over domain + persistence
│           └── unit_of_work.py        # Unit of Work pattern implementation
├── tests/                             # Test suite (pytest-based)
├── docker-compose.yml                 # Production Docker Compose definition
├── Dockerfile                         # Docker image definition
├── Makefile                           # Build, run, and test automation
├── requirements.txt                   # Runtime dependencies
├── requirements-dev.txt               # Dev and test dependencies
└── pytest.ini                         # Pytest configuration
```






