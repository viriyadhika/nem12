from typing import List

from app.utils import logger
from . import get_connection


def run(sqls: List[str]):
    connection = get_connection()
    cursor = connection.cursor()
    for sql in sqls:
        try:
            cursor.execute(sql)
            connection.commit()
            logger.info(f"Execution successful: {sql}")
        except Exception as ex:
            logger.error(f"Error in processing query {sql} {ex}")
            connection.rollback()

    cursor.close()
    connection.close()
