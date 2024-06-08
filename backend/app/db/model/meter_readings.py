from dataclasses import dataclass

meter_reading_table = "meter_readings"


class MeterReadingField:
    nmi = "nmi"
    timestamp = "timestamp"
    consumption = "consumption"


@dataclass
class MeterReading:
    nmi: str
    timestamp: str
    consumption: float
