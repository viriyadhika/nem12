import csv
from typing import List

from .mock.generate_nmi_details import generate_nmi_details
from .models import Record200
from .parser import RowParser
from .generate_sql import generate_meter_reading_sql
from app.utils import logger


def generate_and_write_result(record_200: List[Record200]):
    queries = generate_meter_reading_sql(record_200, True)
    with open("app/files/res.txt", "a") as file:
        for query in queries:
            file.write(query)
            file.write("\n")


def wipe_output_file():
    with open("app/files/res.txt", "w"):
        pass


def get_sql_from_nim12():

    wipe_output_file()

    with open("app/files/out.csv") as file:
        file_reader = csv.reader(file, delimiter=",")
        parser = RowParser()
        batch_size = 10000
        row_count = 0
        batch_count = 1
        for row in file_reader:
            # Process exisitng data first before parsing this row
            if parser.is_200(row) and (row_count / batch_size - batch_count) > 0:
                generate_and_write_result(parser.get_result())
                logger.info(f"{row_count} rows processed")
                parser.clear_result()
                batch_count += 1

            parser.parse_row(row)
            row_count += 1

        # Last batch
        generate_and_write_result(parser.get_result())
