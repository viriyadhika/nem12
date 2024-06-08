import csv

from app.parser import RowParser
from .db.generate_sql import generate_meter_reading_sql


if __name__ == "__main__":
    with open("app/files/NEM12#000000000000001#CNRGYMDP#NEMMCO.csv") as file:
        file_reader = csv.reader(file, delimiter=",")
        parser = RowParser()
        for row in file_reader:
            parser.parse_row(row)

        query = generate_meter_reading_sql(parser.get_result())
        print("\n".join(query))
