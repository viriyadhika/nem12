import csv
from typing import List

from app.utils.files import get_input_file_name, get_result_file_name, get_upload_path

from .mock.generate_nmi_details import generate_nmi_details
from .models import Record200
from .parser import RowParser
from .generate_sql import generate_meter_reading_sql
from app.utils import logger


def generate_and_write_result(record_200: List[Record200], task_id: str):
    queries = generate_meter_reading_sql(record_200, True)
    with open(get_upload_path(get_result_file_name(task_id)), "a") as file:
        for query in queries:
            file.write(query)
            file.write("\n")


def generate_output_file(task_id: str):
    with open(get_upload_path(get_result_file_name(task_id)), "w"):
        pass


def get_sql_from_nim12(task_id: str):

    generate_output_file(task_id)

    with open(get_upload_path(get_input_file_name(task_id))) as file:
        file_reader = csv.reader(file, delimiter=",")
        parser = RowParser()
        batch_size = 10000
        row_count = 0
        batch_count = 1
        for row in file_reader:
            # Process exisitng data first before parsing this row
            if parser.is_200(row) and (row_count / batch_size - batch_count) > 0:
                generate_and_write_result(parser.get_result(), task_id)
                logger.info(f"{row_count} rows processed")
                parser.clear_result()
                batch_count += 1

            parser.parse_row(row)
            row_count += 1

        # Last batch
        generate_and_write_result(parser.get_result(), task_id)
