#!/usr/bin/env python3
"""
Database bootstrap script.
Creates the database (if PostgreSQL) and runs migrations.
"""
import sys
import os
import subprocess
from urllib.parse import urlparse

# Only import psycopg2 if needed (for PostgreSQL)
try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

def parse_database_url(url: str):
    """Parse database URL and return components."""
    parsed = urlparse(url)
    
    # Handle postgresql+asyncpg:// and postgresql://
    if url.startswith("postgresql+asyncpg://"):
        url = url.replace("postgresql+asyncpg://", "postgresql://")
        parsed = urlparse(url)
    
    return {
        "scheme": parsed.scheme,
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 5432,
        "user": parsed.username or "postgres",
        "password": parsed.password or "",
        "database": parsed.path.lstrip("/") if parsed.path else None,
    }

def database_exists(host, port, user, password, database):
    """Check if PostgreSQL database exists."""
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database="postgres"  # Connect to default database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (database,)
        )
        exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        return exists
    except psycopg2.OperationalError as e:
        error_str = str(e)
        if "Connection refused" in error_str or "could not connect" in error_str.lower():
            print(f"\n✗ Error: Cannot connect to PostgreSQL server at {host}:{port}")
            print("   PostgreSQL may not be running.")
            print("\n   To start PostgreSQL:")
            print("   - macOS (Homebrew): brew services start postgresql@14")
            print("   - Linux (systemd): sudo systemctl start postgresql")
            print("   - Or check: pg_isready -h localhost -p 5432")
        elif "does not exist" in error_str.lower() or "FATAL" in error_str:
            print(f"\n✗ Error: PostgreSQL user '{user}' does not exist or authentication failed")
            print(f"\n   On macOS with Homebrew, the default user is your macOS username.")
            print(f"   Try updating your DATABASE_URL to use your username instead of 'postgres':")
            import getpass
            current_user = getpass.getuser()
            print(f"   DATABASE_URL=postgresql://{current_user}@localhost:5432/snake_game")
            print(f"\n   Or create the 'postgres' user:")
            print(f"   createuser -s postgres")
        else:
            print(f"Error checking database existence: {e}")
        return False
    except Exception as e:
        print(f"Error checking database existence: {e}")
        return False

def create_database(host, port, user, password, database):
    """Create PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database="postgres"  # Connect to default database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        cursor.execute(f'CREATE DATABASE "{database}"')
        cursor.close()
        conn.close()
        print(f"✓ Database '{database}' created successfully")
        return True
    except psycopg2.OperationalError as e:
        error_str = str(e)
        if "Connection refused" in error_str or "could not connect" in error_str.lower():
            print(f"\n✗ Error: Cannot connect to PostgreSQL server at {host}:{port}")
            print("   PostgreSQL may not be running.")
            print("\n   To start PostgreSQL:")
            print("   - macOS (Homebrew): brew services start postgresql@14")
            print("   - Linux (systemd): sudo systemctl start postgresql")
            print("   - Or check: pg_isready -h localhost -p 5432")
        elif "does not exist" in error_str.lower() or "FATAL" in error_str:
            print(f"\n✗ Error: PostgreSQL user '{user}' does not exist or authentication failed")
            print(f"\n   On macOS with Homebrew, the default user is your macOS username.")
            print(f"   Try updating your DATABASE_URL to use your username instead of 'postgres':")
            import getpass
            current_user = getpass.getuser()
            print(f"   DATABASE_URL=postgresql://{current_user}@localhost:5432/snake_game")
            print(f"\n   Or create the 'postgres' user:")
            print(f"   createuser -s postgres")
        else:
            print(f"Error creating database: {e}")
        return False
    except psycopg2.errors.DuplicateDatabase:
        print(f"✓ Database '{database}' already exists")
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def run_migrations():
    """Run Alembic migrations."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try to use venv's alembic if available
    venv_alembic = os.path.join(script_dir, "venv", "bin", "alembic")
    if os.path.exists(venv_alembic):
        alembic_cmd = venv_alembic
    else:
        alembic_cmd = "alembic"
    
    try:
        result = subprocess.run(
            [alembic_cmd, "upgrade", "head"],
            cwd=script_dir,
            check=True,
            capture_output=True,
            text=True
        )
        print("✓ Database migrations applied successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: alembic command not found. Make sure you're in a virtual environment")
        print("or install dependencies with: pip install -r requirements.txt")
        return False

def bootstrap_sqlite():
    """Bootstrap SQLite database (just run migrations)."""
    print("Detected SQLite database")
    print("Running migrations...")
    return run_migrations()

def bootstrap_postgresql(db_info):
    """Bootstrap PostgreSQL database."""
    if not PSYCOPG2_AVAILABLE:
        print("Error: psycopg2 is required for PostgreSQL but not installed.")
        print("Install it with: pip install psycopg2-binary")
        return False
    
    print("Detected PostgreSQL database")
    print(f"Host: {db_info['host']}:{db_info['port']}")
    print(f"User: {db_info['user']}")
    print(f"Database: {db_info['database']}")
    
    # Check if database exists
    print("\nChecking if database exists...")
    if database_exists(
        db_info['host'],
        db_info['port'],
        db_info['user'],
        db_info['password'],
        db_info['database']
    ):
        print(f"✓ Database '{db_info['database']}' already exists")
    else:
        print(f"Database '{db_info['database']}' does not exist")
        print("Creating database...")
        if not create_database(
            db_info['host'],
            db_info['port'],
            db_info['user'],
            db_info['password'],
            db_info['database']
        ):
            return False
    
    # Run migrations
    print("\nRunning migrations...")
    return run_migrations()

def main():
    """Main bootstrap function."""
    # Load environment variables
    from app.core.config import settings
    
    database_url = settings.DATABASE_URL
    print(f"Database URL: {database_url.split('@')[-1] if '@' in database_url else database_url}")
    print()
    
    # Parse database URL
    db_info = parse_database_url(database_url)
    
    # Bootstrap based on database type
    if db_info['scheme'] == 'sqlite':
        success = bootstrap_sqlite()
    elif db_info['scheme'] == 'postgresql':
        if not db_info['database']:
            print("Error: Database name not specified in DATABASE_URL")
            sys.exit(1)
        success = bootstrap_postgresql(db_info)
    else:
        print(f"Error: Unsupported database scheme: {db_info['scheme']}")
        print("Supported schemes: sqlite, postgresql")
        sys.exit(1)
    
    if success:
        print("\n✓ Database bootstrap completed successfully!")
        sys.exit(0)
    else:
        print("\n✗ Database bootstrap failed")
        sys.exit(1)

if __name__ == "__main__":
    main()

