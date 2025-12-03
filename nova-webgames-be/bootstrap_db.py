#!/usr/bin/env python3
"""
Database bootstrap script.
Creates the database (if PostgreSQL) and runs migrations.
"""
import sys
import os
import subprocess
from urllib.parse import urlparse
from datetime import datetime

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
    print(f"Running migrations from: {script_dir}")
    
    # Try to use venv's alembic if available
    venv_alembic = os.path.join(script_dir, "venv", "bin", "alembic")
    if os.path.exists(venv_alembic):
        alembic_cmd = venv_alembic
        print(f"Using venv alembic: {alembic_cmd}")
    else:
        alembic_cmd = "alembic"
        print(f"Using system alembic: {alembic_cmd}")
    
    # Check if alembic exists
    if not os.path.exists(alembic_cmd) and alembic_cmd != "alembic":
        # Try to find alembic in PATH
        import shutil
        alembic_path = shutil.which("alembic")
        if alembic_path:
            alembic_cmd = alembic_path
            print(f"Found alembic in PATH: {alembic_cmd}")
        else:
            print("Error: alembic command not found. Make sure you're in a virtual environment")
            print("or install dependencies with: pip install -r requirements.txt")
            return False
    
    print("Executing: alembic upgrade head")
    try:
        result = subprocess.run(
            [alembic_cmd, "upgrade", "head"],
            cwd=script_dir,
            check=True,
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout to prevent hanging
        )
        print("✓ Database migrations applied successfully")
        if result.stdout:
            print("Migration output:")
            print(result.stdout)
        return True
    except subprocess.TimeoutExpired:
        print("✗ ERROR: Migration command timed out after 60 seconds")
        print("This suggests the migration is hanging or taking too long")
        return False
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running migrations: {e}")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        print("✗ Error: alembic command not found. Make sure you're in a virtual environment")
        print("or install dependencies with: pip install -r requirements.txt")
        return False

def bootstrap_sqlite():
    """Bootstrap SQLite database (just run migrations)."""
    print("Detected SQLite database")
    
    # Extract database file path from DATABASE_URL
    from app.core.config import settings
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite:///./"):
        db_file = db_url.replace("sqlite:///./", "")
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_file)
        print(f"Database file path: {db_path}")
        if os.path.exists(db_path):
            print(f"✓ Database file exists: {db_file}")
            file_size = os.path.getsize(db_path)
            print(f"  File size: {file_size} bytes")
        else:
            print(f"⚠ Database file does not exist yet: {db_file}")
    
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
    print("=" * 50)
    print("Database Bootstrap Script")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Script location: {os.path.abspath(__file__)}")
    print()
    
    # Load environment variables
    try:
        from app.core.config import settings
        database_url = settings.DATABASE_URL
        print(f"Database URL: {database_url.split('@')[-1] if '@' in database_url else database_url}")
        print()
    except Exception as e:
        print(f"✗ ERROR: Failed to load settings: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Parse database URL
    try:
        db_info = parse_database_url(database_url)
        print(f"Parsed database info:")
        print(f"  Scheme: {db_info['scheme']}")
        print(f"  Host: {db_info['host']}")
        print(f"  Port: {db_info['port']}")
        print(f"  User: {db_info['user']}")
        print(f"  Database: {db_info['database']}")
        print()
    except Exception as e:
        print(f"✗ ERROR: Failed to parse database URL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Bootstrap based on database type
    try:
        if db_info['scheme'] == 'sqlite':
            success = bootstrap_sqlite()
        elif db_info['scheme'] == 'postgresql':
            if not db_info['database']:
                print("✗ Error: Database name not specified in DATABASE_URL")
                sys.exit(1)
            success = bootstrap_postgresql(db_info)
        else:
            print(f"✗ Error: Unsupported database scheme: {db_info['scheme']}")
            print("Supported schemes: sqlite, postgresql")
            sys.exit(1)
    except Exception as e:
        print(f"✗ ERROR: Exception during bootstrap: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    if success:
        print("\n" + "=" * 50)
        print("✓ Database bootstrap completed successfully!")
        print("=" * 50)
        sys.exit(0)
    else:
        print("\n" + "=" * 50)
        print("✗ Database bootstrap failed")
        print("=" * 50)
        sys.exit(1)

if __name__ == "__main__":
    main()

