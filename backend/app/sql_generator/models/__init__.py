from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class IntervalRecord:
    date: datetime
    value: float


@dataclass
class Record300:
    date: datetime
    interval_records: List[IntervalRecord]


@dataclass
class Record200:
    """
    Class to keep 200 records and its children
    """

    nmi: str
    record_300: List[Record300]
    interval: int
