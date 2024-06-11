import csv
from typing import List

from app.mock.generate_nmi_details import generate_nmi_details
from app.models import Record200
from app.parser import RowParser
from .db.generate_sql import generate_meter_reading_sql


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
                print(f"{row_count} rows processed", flush=True)
                parser.clear_result()
                batch_count += 1

            parser.parse_row(row)
            row_count += 1

        # Last batch
        generate_and_write_result(parser.get_result())


if __name__ == "__main__":
    get_sql_from_nim12()
    # generate_nmi_details(5000)
