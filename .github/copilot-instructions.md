# Copilot Instructions for hse-25-winter

## Project Overview
This is a **distributed system project** featuring a microservices architecture with two independent backends (Django and Spring Boot) serving the same Todo API. Both connect to shared PostgreSQL and are orchestrated via Docker Compose and Kubernetes.

## Architecture

### Core Components
- **Django Backend** (`djangobackend/`) - Python REST API using Django 5.1.3
- **Spring Boot App** (`starterapp/`) - Java REST API using Spring Boot 3.5.6
- **PostgreSQL** - Shared database for both backends (port 5432)
- **Kubernetes** (`k8s/`) - Deployment manifests for cloud-native orchestration
- **Docker Compose** - Local development multi-container setup

### Data Flow
1. Both backends implement identical REST endpoints for TodoItems
2. PostgreSQL with credentials: user=`postgres`, password=`mysecretpassword`
3. Django connects via `DB_HOST` environment variable (defaults to 'postgres' for Docker)
4. Backends run independently on ports 8000 (Django) and 8080 (Spring)

## Critical Patterns

### REST API Design (RMM Levels)
Both backends follow **Richardson Maturity Model** progression:
- **Level 0 (POX)**: Legacy endpoints like `/gettodos`, `/getTodoById` (for compatibility)
- **Level 1 (Resources)**: `/todos`, `/todos/{id}` - proper resource naming
- **Level 2 (HTTP Methods)**: GET, POST, PUT, DELETE with appropriate status codes (201 for create, 204 for delete)

**Django implementation** ([api/views.py](api/views.py)): Uses `@csrf_exempt` decorators and function-based views with explicit HTTP method routing
**Spring implementation** ([TodoController.java](starterapp/src/main/java/com/example/demo/TodoController.java)): Uses annotations (@GetMapping, @PostMapping, @PutMapping, @DeleteMapping) with `@CrossOrigin(origins = "*")`

### Database Models
TodoItem fields:
```
title (CharField/String, max 200)
description (TextField/String, blank allowed)
completed (Boolean, default False)
created_at / updated_at (auto-timestamped)
id (auto-incrementing primary key)
```
Django includes `to_dict()` method for API serialization; Spring uses entity directly.

### Important Implementation Notes
- Django PUT handler explicitly checks `if 'completed' in data` before converting to boolean
- Spring TodoService uses JPA repositories (implicit from naming pattern)
- Both ignore CSRF for testing purposes (`@csrf_exempt` in Django, development mode)

## Development Workflows

### Local Development
```bash
cd djangobackend
docker-compose up                    # Starts Django + PostgreSQL
python manage.py migrate            # Run migrations (also in docker-compose)
python manage.py runserver          # Alternative: manual start
```

### Database Setup
- Django migrations auto-run in docker-compose command
- PostgreSQL auto-initializes via docker-compose with named volume `postgres_data`
- Environment variable `DB_HOST=postgres` for Docker networking

### Building & Deployment
- **Django**: Dockerfile uses `python:*` base, runs migrate + runserver
- **Spring**: Maven build via `./mvnw` (included)
- **Kubernetes**: Apply manifests in order - postgres first, then django deployment/service

## Project Conventions

1. **Environment Configuration**: Critical settings via env vars (DB_HOST, DEBUG mode)
2. **Django Dependencies**: Minimal set - only Django 5.1.3 and psycopg2
3. **Spring Dependency Injection**: `@Autowired` pattern for service injection
4. **API Response Format**: JSON objects with fields matching TodoItem properties
5. **Status Codes**: 201 (created), 204 (deleted), 404 (not found), 200 (success)
6. **Cross-Origin**: Django disables CSRF; Spring enables full CORS for testing

## Key File References
- [djangobackend/api/models.py](djangobackend/api/models.py) - TodoItem ORM model
- [djangobackend/api/views.py](djangobackend/api/views.py) - Django REST endpoints
- [djangobackend/djangobackend/settings.py](djangobackend/djangobackend/settings.py) - DB config and middleware
- [starterapp/src/main/java/com/example/demo/TodoService.java](starterapp/src/main/java/com/example/demo/TodoService.java) - Spring service layer
- [docker-compose.yaml](docker-compose.yaml) - Local env orchestration
- [k8s/django-deployment.yaml](k8s/django-deployment.yaml) - Production deployment template

## Testing Tips
- Django test file: [djangobackend/api/tests.py](djangobackend/api/tests.py)
- Spring test file: [starterapp/src/test/java/com/example/demo/DemoApplicationTests.java](starterapp/src/test/java/com/example/demo/DemoApplicationTests.java)
- Use `curl` or Postman to test endpoints directly after `docker-compose up`
- Verify database connection via `DB_HOST` env var is set correctly
