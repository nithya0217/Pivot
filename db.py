import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "Missing DATABASE_URL environment variable. "
        "Set DATABASE_URL in .env or in the deployment environment."
    )

# Connection pool
pool = None

async def init_db():
    """Initialize the database connection pool"""
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            DATABASE_URL,
            min_size=5,
            max_size=20,
            command_timeout=60,
            ssl='require',
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
