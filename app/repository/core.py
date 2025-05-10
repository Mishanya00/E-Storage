from contextlib import asynccontextmanager
from psycopg import AsyncConnection


@asynccontextmanager
async def get_db_connection(config: str):
    conn = None
    try:
        conn = await AsyncConnection.connect(config)
        yield conn
    except Exception as e:
        print(f"DB Connection failed: {e}")
        raise
    finally:
        if conn:
            await conn.close()