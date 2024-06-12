from app.utils import logger
from typing import List
from ..models import IntervalRecord, Record200, Record300
from .constants import (
    RECORD_200_DAY_IN_MINUTES,
    RECORD_200_INTERVAL_INDEX,
    RECORD_200_NMI_INDEX,
    RECORD_300_DATE_FORMAT,
    RECORD_300_DATE_INDEX,
    RECORD_300_INTERVAL_VALUE_INDEX,
)
from datetime import datetime, timedelta


class RowParser:
    def __init__(self) -> None:
        self.records: List[Record200] = []

    def _parse_200(self, row: List[str]):
        new_record_200 = Record200(
            row[RECORD_200_NMI_INDEX], [], int(row[RECORD_200_INTERVAL_INDEX])
        )
        self.records.append(new_record_200)

    def _parse_300(self, row: List[str]):
        if len(self.records) == 0:
            logger.warn("The current 300 record cannot be correlated to any 200 record")
            return
        last_record = self.records[-1]
        n_interval = (int)(RECORD_200_DAY_IN_MINUTES / last_record.interval)
        date = row[RECORD_300_DATE_INDEX]
        date_obj = datetime.strptime(date, RECORD_300_DATE_FORMAT)
        new_record_300 = Record300(date_obj, [])
        for i in range(n_interval):
            current = i + RECORD_300_INTERVAL_VALUE_INDEX
            if current >= len(row):
                logger.warn("Data is incomplete")
                break
            new_record_300.interval_records.append(
                IntervalRecord(
                    date_obj + timedelta(minutes=i * last_record.interval),
                    float(row[current]),
                )
            )
        last_record.record_300.append(new_record_300)

    def _get_record_indicator(self, row: List[str]):
        return int(row[0])

    def parse_row(self, row: List[str]):
        record_indicator = self._get_record_indicator(row)

        if record_indicator == 200:
            self._parse_200(row)
        if record_indicator == 300:
            self._parse_300(row)

    def is_200(self, row: List[str]) -> bool:
        return self._get_record_indicator(row) == 200

    def get_result(self) -> List[Record200]:
        return self.records

    def clear_result(self):
        self.records = []
