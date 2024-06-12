from typing import List
import psycopg2
from app.utils.env import (
    POSTGRES_DB,
    POSTGRES_HOST,
    POSTGRES_PASSWORD,
    POSTGRES_USER,
    POSTGRES_PORT,
)
from app.utils import logger


def get_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        port=POSTGRES_PORT,
    )


def run(sqls: List[str]):
    connection = get_connection()
    cursor = connection.cursor()
    for sql in sqls:
        try:
            cursor.execute(sql)
            connection.commit()
        except Exception as ex:
            logger.error(f"Error in processing query {sql} {ex}")

    cursor.close()
    connection.close()
