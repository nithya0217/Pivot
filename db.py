import os
from pathlib import Path
import asyncpg
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load .env explicitly from the backend folder regardless of current working directory
dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is not None and DATABASE_URL.strip() == "":
    DATABASE_URL = None

if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "postgres")

    if DB_HOST:
        DB_HOST = DB_HOST.lstrip("@")

    if not DB_PASSWORD or not DB_HOST:
        raise RuntimeError(
            "Missing or invalid database configuration. "
            "Set DATABASE_URL or DB_HOST and DB_PASSWORD in environment variables."
        )

    DATABASE_URL = (
        f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

# Connection pool
pool = None

async def init_db():
    """Initialize the database connection pool"""
    global pool
    if pool is None:
        # Use SSL for production, disable for local dev
        ssl_mode = 'require' if os.getenv('ENV') == 'production' else False
        pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=5,
            max_size=20,
            command_timeout=60,
            ssl=ssl_mode,
        )
    return pool

async def get_db():
    """Get a connection from the pool"""
    if pool is None:
        await init_db()
    return await pool.acquire()

async def close_db():
    """Close the connection pool"""
    global pool
    if pool is not None:
        await pool.close()
        pool = None
