import csv

from app.parser import RowParser


if __name__ == "__main__":
    with open("app/files/NEM12#000000000000001#CNRGYMDP#NEMMCO.csv") as file:
        file_reader = csv.reader(file, delimiter=",")
        parser = RowParser(region="Australia/Sydney")
        for row in file_reader:
            parser.parse_row(row)

        print(parser.get_result())
