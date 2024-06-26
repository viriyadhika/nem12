from random import random
from typing import List
from app.utils import logger


def wipe(file_name: str):
    ## Wipe the file
    with open(file_name, "w"):
        pass


def write_to_file(rows: List[str], file_name: str):
    with open(file_name, "a") as file:
        for row in rows:
            file.write(row)
            file.write("\n")


def get_300_row(cur_date: int):
    row_300 = ["300", str(cur_date)]
    for _ in range(48):
        row_300.append(str(round(random(), 3)))
    row_300.append("A,,,20050310121004")
    return ",".join(row_300)


def generate_nmi_details(num_records: int, file_name: str):
    rows = []
    num = 0

    wipe(file_name)

    for _ in range(num_records):
        padded_num = str(num).zfill(7)
        row_200 = f"200,NEM{padded_num},E1E2,2,E2,,01009,kWh,30,20050610"
        rows.append(row_200)

        start_date = 20050301
        for j in range(20):
            cur_date = start_date + j
            rows.append(get_300_row(cur_date))

        # Empty the memory
        if len(rows) > 10000:
            write_to_file(rows, file_name)
            logger.info(f"{len(rows)} rows generated")
            rows = []

        num += 1

    write_to_file(rows, file_name)
    logger.info(f"{len(rows)} rows generated")
