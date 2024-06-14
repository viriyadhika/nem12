from app.utils import logger
from . import get_connection


def run():
    connection = get_connection()
    cursor = connection.cursor()

    query = """create table meter_readings (
        id uuid default gen_random_uuid() not null,
        "nmi" varchar(10) not null,
        "timestamp" timestamp not null,
        "consumption" numeric not null,
        constraint meter_readings_pk primary key (id),
        constraint meter_readings_unique_consumption unique ("nmi", "timestamp")
        );"""

    try:
        cursor.execute(query)
        connection.commit()
        logger.info("create table successful")
    except Exception as e:
        logger.error(f"create table failed due to {e}")

    cursor.close()
    connection.close()
