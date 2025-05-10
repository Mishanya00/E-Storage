import psycopg
from app.repository.core import get_db_connection
from app.config import DATABASE_URL


async def create_tables():
    commands = (
        """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_pswd VARCHAR(255) NOT NULL
        )
        """,

        """
        CREATE TABLE files (
            file_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            filename VARCHAR(255) NOT NULL,
            path TEXT NOT NULL,
            size BIGINT NOT NULL,
            mime_type VARCHAR(100),
            upload_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
            UNIQUE (user_id, filename)
        )
        """
    )

    async with get_db_connection(DATABASE_URL) as aconn:
        for command in commands:
            try:
                async with aconn.cursor() as acur:
                    await acur.execute(command)
                    await aconn.commit()
            except psycopg.errors.DuplicateTable:
                print(f"table {command.split()[2]} already exists")
                await aconn.rollback()
            except Exception as e:
                print(f"Error executing command: {e}")
                await aconn.rollback()
                raise
