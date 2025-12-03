# AGENTS.md

This file provides context and instructions for AI agents working in this repository.

## Project Structure

This is a monorepo containing:
- **`nova-webgames-be/`** - FastAPI backend (Python 3.7+)
- **`nova-webgames-fe/`** - React frontend (TypeScript, Vite)

The project uses a Makefile for common operations. Always check `make help` for available commands.

## Development Environment Tips

### Initial Setup
- Use `make install` to install dependencies for both frontend and backend
- Backend uses a Python virtual environment at `nova-webgames-be/venv/`
- Frontend uses npm packages in `nova-webgames-fe/node_modules/`
- Always activate the backend venv before running Python commands: `source nova-webgames-be/venv/bin/activate`

### Running Services
- Use `make dev` to start both frontend and backend servers
- Backend runs on port 8000: http://localhost:8000
- Frontend runs on port 5173: http://localhost:5173
- API docs available at: http://localhost:8000/docs
- Use `make stop` to stop all servers

### Docker Development (Recommended)
- Use `make docker-up` to start all services (PostgreSQL, backend, frontend)
- Use `make docker-bootstrap` to set up the database in containers
- Use `make docker-logs` to view logs
- Hot reload works in Docker - code changes are automatically reflected

### Database Setup
- The project supports both PostgreSQL (recommended) and SQLite (development)
- Use `make bootstrap-db` to create the database (if needed) and run migrations
- Database migrations are managed with Alembic in `nova-webgames-be/alembic/`
- Environment variables are configured in `.env` files (see README.md for details)

### Navigating the Codebase
- Backend API routes: `nova-webgames-be/app/api/v1/`
- Backend models: `nova-webgames-be/app/models/`
- Backend schemas: `nova-webgames-be/app/schemas/`
- Frontend components: `nova-webgames-fe/src/components/`
- Frontend services: `nova-webgames-fe/src/services/`
- Frontend tests: `nova-webgames-fe/src/**/__tests__/` and `nova-webgames-fe/e2e/`

## Testing Instructions

### Backend Tests
- Run backend tests: `make test-be` or `cd nova-webgames-be && pytest`
- Tests are located in `nova-webgames-be/tests/`
- Ensure virtual environment is activated before running tests
- All tests should pass before committing

### Frontend Unit Tests
- Run frontend unit tests: `make test-fe` or `cd nova-webgames-fe && npm test`
- Tests use Vitest and React Testing Library
- Run in watch mode: `cd nova-webgames-fe && npm run test:watch`
- Run with coverage: `cd nova-webgames-fe && npm run test:coverage`

### E2E Tests
- Run E2E tests: `make test-e2e` (automatically starts servers)
- E2E tests use Playwright and are in `nova-webgames-fe/e2e/`
- Run in UI mode: `make test-e2e-ui`
- Run with visible browser: `make test-e2e-headed`
- Debug E2E tests: `make test-e2e-debug`
- Install Playwright browsers: `make install-playwright`

### Test All
- Run all tests (unit + E2E): `make test-all`
- Always run tests before creating a PR

## Code Quality

### Backend
- Use type hints in Python code
- Follow FastAPI best practices
- Run `pytest` to ensure all tests pass
- Check for linting errors (if configured)

### Frontend
- Use TypeScript strictly (no `any` types unless necessary)
- Follow React best practices and hooks patterns
- Run `npm test` to ensure all tests pass
- Run `npm run build` to check for TypeScript errors
- Run `npm run lint` if available

## Database Migrations

### Creating Migrations
- Navigate to backend: `cd nova-webgames-be`
- Activate venv: `source venv/bin/activate`
- Create migration: `alembic revision --autogenerate -m "description"`
- Review the generated migration file before applying

### Applying Migrations
- Use `make migrate` to apply all pending migrations
- Or directly: `cd nova-webgames-be && alembic upgrade head`
- In Docker: `make docker-migrate`

### Rolling Back
- Downgrade one revision: `make migrate-down`
- Or directly: `cd nova-webgames-be && alembic downgrade -1`

## Pull Request Instructions

### PR Title Format
- Use descriptive titles that explain what the PR does
- Examples:
  - "Add user authentication endpoint"
  - "Fix leaderboard sorting bug"
  - "Update frontend to use new API endpoint"

### Pre-PR Checklist
1. **Run all tests**: `make test-all`
2. **Check TypeScript compilation**: `cd nova-webgames-fe && npm run build`
3. **Ensure database migrations are up to date**: `make migrate`
4. **Verify code works in Docker** (if applicable): `make docker-up && make docker-bootstrap`
5. **Review your changes** - ensure no debug code, console.logs, or commented code remains

### PR Description
- Describe what the PR does and why
- Mention any breaking changes
- Include testing instructions if applicable
- Reference related issues if any

### Commit Messages
- Use clear, descriptive commit messages
- Follow conventional commit format when possible (feat:, fix:, docs:, etc.)

## Common Tasks

### Adding a New API Endpoint
1. Add route handler in `nova-webgames-be/app/api/v1/`
2. Add Pydantic schema in `nova-webgames-be/app/schemas/`
3. Add database model if needed in `nova-webgames-be/app/models/`
4. Create migration if model changed: `alembic revision --autogenerate -m "add new model"`
5. Add tests in `nova-webgames-be/tests/`
6. Update OpenAPI spec (auto-generated, but verify)

### Adding a New Frontend Component
1. Create component in `nova-webgames-fe/src/components/`
2. Add CSS file if needed (same directory)
3. Add tests in `__tests__/` subdirectory
4. Update routing in `nova-webgames-fe/src/App.tsx` if needed

### Updating Dependencies
- Backend: Edit `nova-webgames-be/requirements.txt`, then `cd nova-webgames-be && venv/bin/pip install -r requirements.txt`
- Frontend: Edit `nova-webgames-fe/package.json`, then `cd nova-webgames-fe && npm install`

## Environment Variables

### Backend (`.env` in `nova-webgames-be/`)
- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret key
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time
- `SESSION_TIMEOUT` - Session timeout in seconds

### Frontend (`.env` in `nova-webgames-fe/`)
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000/api/v1)

## Important Notes

- **Never commit sensitive data** (API keys, passwords, etc.)
- **Always run tests** before committing
- **Database migrations** should be reviewed before applying
- **TypeScript errors** must be fixed before committing frontend changes
- **Hot reload** works in both Docker and local development
- **The Makefile** is the source of truth for common commands - use it instead of remembering exact commands

## Getting Help

- Check `make help` for available commands
- Review `README.md` for project overview
- Check `nova-webgames-be/README.md` for backend-specific details
- Review test files for examples of how to use the codebase

## Scratch files

- if you need to use a scratch document for thinking or documentation, place it in the `/scratch` directory. 

## Documentation

- When making changes that affect the setup or tools available in this repository, document those changes in appropriate documentation files. 