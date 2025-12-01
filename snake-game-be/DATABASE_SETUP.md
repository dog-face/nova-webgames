# Database Setup Guide

## Quick Fix for Current Issue

You're seeing an error because PostgreSQL on macOS (Homebrew) uses your **macOS username** as the default database user, not `postgres`.

### Solution

Create a `.env` file in `snake-game-be/` with your macOS username:

```bash
cd snake-game-be
cat > .env << EOF
DATABASE_URL=postgresql://noahvito@localhost:5432/snake_game
SECRET_KEY=your-secret-key-here-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=1440
SESSION_TIMEOUT=300
EOF
```

Then run:
```bash
make bootstrap-db
```

## Finding Your PostgreSQL Username

To find your PostgreSQL username:
```bash
psql -l
```

Look at the "Owner" column - that's your PostgreSQL username.

## Complete Setup Steps

1. **Start PostgreSQL** (if not running):
   ```bash
   brew services start postgresql@14
   pg_isready -h localhost -p 5432
   ```

2. **Create `.env` file** in `snake-game-be/`:
   ```env
   # Use your macOS username (found via: psql -l)
   DATABASE_URL=postgresql://your_username@localhost:5432/snake_game
   SECRET_KEY=your-secret-key-here-change-in-production
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   SESSION_TIMEOUT=300
   ```

3. **Bootstrap the database**:
   ```bash
   make bootstrap-db
   ```

This will:
- Check if the `snake_game` database exists
- Create it if it doesn't exist
- Run all migrations to set up tables

## Alternative: Create a 'postgres' User

If you prefer to use the `postgres` user:

```bash
createuser -s postgres
```

Then your `.env` can use:
```env
DATABASE_URL=postgresql://postgres@localhost:5432/snake_game
```

## Troubleshooting

**"role does not exist" error:**
- Use your macOS username in `DATABASE_URL` (found via `psql -l`)
- Or create the `postgres` user: `createuser -s postgres`

**"Connection refused" error:**
- Start PostgreSQL: `brew services start postgresql@14`
- Check status: `pg_isready -h localhost -p 5432`

**"Permission denied" error:**
- Ensure your user has permission to create databases
- On macOS with Homebrew, your user should have superuser privileges by default

