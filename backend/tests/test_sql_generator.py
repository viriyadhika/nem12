from datetime import datetime
from random import random
from app.sql_generator.generate_sql import generate_meter_reading_sql
from app.sql_generator.models import IntervalRecord, Record200, Record300
from app.sql_generator.parser import RowParser


class TestGenerateSQL:
    def test_generate_sql(self):
        records = Record200("nmi1", [], 30)
        new_record_300 = Record300(datetime.strptime("20240615", "%Y%m%d"), [])
        for i in range(48):
            minute_from_midnight = i * 30
            hour = minute_from_midnight // 60
            minutes = minute_from_midnight - hour * 60
            new_interval = IntervalRecord(
                datetime.strptime(f"20240615 {hour:02d}:{minutes:02d}", "%Y%m%d %H:%M"),
                random(),
            )
            new_record_300.interval_records.append(new_interval)
        records.record_300.append(new_record_300)

        result = generate_meter_reading_sql([records])
        for idx, item in enumerate(result):
            corresponding_interval_record = records.record_300[0].interval_records[idx]
            date = corresponding_interval_record.date.strftime("%Y-%m-%d %H:%M")
            value = corresponding_interval_record.value
            expectation = f'INSERT INTO "meter_readings" ("nmi","timestamp","consumption") VALUES (\'nmi1\',\'{date}\',{value})'
            assert item == expectation


class TestParsingSample:
    def test_parser(self):
        sample_data = [
            "200,NEM1201009,E1E2,1,E1,N1,01009,kWh,30,20050610",
            "300,20050301,0,0,0,0,0,0,0,0,0,0,0,0,0.461,0.810,0.568,1.234,1.353,1.507,1.344,1.773,0.848,1.271,0.895,1.327,1.013,1.793,0.988,0.985,0.876,0.555,0.760,0.938,0.566,0.512,0.970,0.760,0.731,0.615,0.886,0.531,0.774,0.712,0.598,0.670,0.587,0.657,0.345,0.231,A,,,20050310121004,20050310182204",
        ]
        parser = RowParser()
        for item in sample_data:
            parser.parse_row(item.split(","))

        result = parser.get_result()
        assert len(result) == 1
        assert result[0].nmi == "NEM1201009"
        assert result[0].interval == 30
        assert len(result[0].record_300) == 1
        assert len(result[0].record_300[0].interval_records) == 48
        assert result[0].record_300[0].interval_records[0].value == 0
        assert result[0].record_300[0].interval_records[-1].value == 0.231
