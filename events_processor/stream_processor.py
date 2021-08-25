
from kinesis_records import KinesisRecords


class StreamProcessor:
    def process(self, event):
        kinesis_records = KinesisRecords()
        if kinesis_records.load_configuration() == False:
            return False
        return kinesis_records.process_records(event)
