# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based thought management system that allows users to capture, organize, and share their ideas. It features dual authentication (username/password + Google OAuth), public/private thoughts, tagging, search functionality, and a modern responsive UI.

## Development Commands

### Setup and Installation
```bash
# Setup virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Alternative using Makefile
make install
```

### Database Management
```bash
# Initialize database
python manage.py init-db

# Seed with default admin user (admin/admin123)
python manage.py seed-db

# List all users
python manage.py list-users

# Delete a user
python manage.py delete-user <username>

# Database migrations
flask db migrate -m "Description of changes"
flask db upgrade
flask db downgrade
```

### Development Server
```bash
# Run the application
python run.py
# Available at http://localhost:5000
```

### Code Quality and Testing
```bash
# Format code
make format
# Runs: black . && isort .

# Run linting
make lint
# Runs: black ., isort ., flake8 ., pylint app/

# Run tests
make test
pytest tests/
pytest --cov=app --cov-report=term-missing tests/

# Quick format and flake8 check
make quick

# Full code quality check
make full

# Setup development environment
make dev-setup
```

## Application Architecture

### Application Factory Pattern
The app uses Flask's application factory pattern in `app/__init__.py` with blueprint-based organization:

- `app/auth/` - Authentication (login, register, profile, Google OAuth)
- `app/main/` - Core thought management functionality
- `app/api/` - Basic API endpoints
- `app/models.py` - SQLAlchemy models (User, Thought) with helper functions
- `app/config.py` - Configuration classes for different environments

### Database Models
- **User**: Authentication with both local and OAuth support (Google)
- **Thought**: Core entity with title, content, category, tags, and public/private visibility

### Key Features
- Blueprint-based modular architecture
- SQLAlchemy ORM with Flask-Migrate for database versioning
- Flask-Login for session management
- WTForms for form validation and CSRF protection
- Template filters (e.g., `nl2br` for newline to `<br>` conversion)
- Pagination support for thought listings
- Full-text search across titles, content, and tags

### Configuration
Uses environment variables loaded via python-dotenv:
- `SECRET_KEY` - Flask secret key
- `DATABASE_URL` - Database connection string (defaults to SQLite)
- `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` - Google OAuth credentials

### Testing
- Uses pytest with pytest-cov for coverage
- Test configuration in `pytest.ini`
- Testing config uses in-memory SQLite database

## Code Quality Tools

The project is configured with comprehensive linting and formatting:
- **Black** for code formatting (88-character line length)
- **isort** for import sorting
- **flake8** for linting
- **pylint** for additional code analysis (many rules disabled for Flask patterns)
- **mypy** for type checking (configured in pyproject.toml)
- **pre-commit** hooks available

Run `make lint` before committing changes.
