from dataclasses import dataclass
from typing import List


@dataclass
class IntervalRecord:
    timestamp: int
    value: float


@dataclass
class Record300:
    start_timestamp: int
    interval_records: List[IntervalRecord]


@dataclass
class Record200:
    """
    Class to keep 200 records and its children
    """

    nmi: str
    record_300: List[Record300]
    interval: int
