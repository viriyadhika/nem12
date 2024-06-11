from typing import List
from app.models import Record200
from .model.meter_readings import MeterReading, MeterReadingField, meter_reading_table
from pypika import Table, PostgreSQLQuery


def convert_meter_reading_to_insert_sql(
    reading: MeterReading, disable_escaping: bool
) -> str:
    if disable_escaping:
        return (
            f"INSERT INTO {meter_reading_table} ({MeterReadingField.nmi}, {MeterReadingField.timestamp}, {MeterReadingField.consumption}) "
            f"VALUES ('{reading.nmi}', '{reading.timestamp}', '{reading.consumption}')"
        )

    table = Table(meter_reading_table)
    return str(
        PostgreSQLQuery.into(table)
        .columns(
            MeterReadingField.nmi,
            MeterReadingField.timestamp,
            MeterReadingField.consumption,
        )
        .insert(reading.nmi, reading.timestamp, reading.consumption)
    )


def generate_meter_reading_sql(
    records: List[Record200], disable_escaping=False
) -> List[str]:
    result: List[str] = []
    for record in records:
        for record_300 in record.record_300:
            for interval_record in record_300.interval_records:
                new_reading = MeterReading(
                    nmi=record.nmi,
                    timestamp=interval_record.date.strftime("%Y-%m-%d %H:%M"),
                    consumption=interval_record.value,
                )
                item = convert_meter_reading_to_insert_sql(
                    new_reading, disable_escaping
                )
                result.append(item)

    return result
