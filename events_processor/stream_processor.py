
from kinesis_records import KinesisRecords


class StreamProcessor:
    def __init__(self):
        print("Kinesis Consumer")

    def subscribe(self):
        print("kinesis consumer subscribed")
        return True

    def process(self, event):
        kinesis_records = KinesisRecords()
        result = kinesis_records.process_records(event)
