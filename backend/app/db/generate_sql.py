from typing import List
from app.models import Record200
from .model.meter_readings import MeterReading, MeterReadingField, meter_reading_table
from pypika import Query, Table


def convert_meter_reading_to_insert_sql(reading: MeterReading) -> str:
    table = Table(meter_reading_table)

    return str(
        Query.into(table)
        .columns(
            MeterReadingField.nmi,
            MeterReadingField.timestamp,
            MeterReadingField.consumption,
        )
        .insert(reading.nmi, reading.timestamp, reading.consumption)
    )


def generate_meter_reading_sql(records: List[Record200]) -> List[str]:
    result: List[str] = []
    for record in records:
        for record_300 in record.record_300:
            for interval_record in record_300.interval_records:
                new_reading = MeterReading(
                    nmi=record.nmi,
                    timestamp=interval_record.date.strftime("%Y-%m-%d %H:%M"),
                    consumption=interval_record.value,
                )
                result.append(convert_meter_reading_to_insert_sql(new_reading))

    return result
