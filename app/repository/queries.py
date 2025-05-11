from psycopg import rows

from app.repository.core import get_db_connection
from app.config import DATABASE_URL


async def get_user_by_email(email: str):
    async with get_db_connection(DATABASE_URL) as aconn:
        # rows.dict_row to generate dictionary as a result of query
        async with aconn.cursor(row_factory=rows.dict_row) as acur:
            sql = """
                    SELECT user_id, email, hashed_pswd FROM users
                    WHERE email = %s
                """
            await acur.execute(sql, [email])
            record = await acur.fetchone()
            return record


async def create_user(email: str, password_hash: str):
    async with get_db_connection(DATABASE_URL) as aconn:
        async with aconn.cursor() as acur:
            sql = f"""
                    INSERT INTO users(email, hashed_pswd)
                    VALUES (%s, %s)
                """
            await acur.execute(sql, [email, password_hash])
        await aconn.commit()


async def add_file(user_id: int, filename: str, filepath: str, size:int, mimetype: str):
    async with get_db_connection(DATABASE_URL) as aconn:
        async with aconn.cursor() as acur:
            sql = """
                INSERT INTO files(user_id, filename, path, size, mime_type)
                VALUES (%s, %s, %s, %s, %s)      
            """
            await acur.execute(sql, [user_id, filename, filepath, size, mimetype])
        await aconn.commit()


async def get_files_by_user(email: str, password_hash: str):
    async with get_db_connection(DATABASE_URL) as aconn:
        async with aconn.cursor() as acur:
            pass